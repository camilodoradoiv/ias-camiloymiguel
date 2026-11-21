"""
PUNTO 1: IA generativa de Machine Learning.

Una pregunta -> respuesta en texto + voz + fotos reales + videos reales.

Cómo piensa (en este orden, usa el primero que esté disponible):
  1. Claude (clave de Anthropic)       -> razona de verdad.
  2. Gemini (clave GRATIS de Google)   -> razona de verdad.
  3. Ollama (modelo local, sin clave)  -> razona de verdad, sin internet.
  4. Modo básico (Wikipedia)           -> solo resume un artículo; NO razona.

Fotos: Wikimedia Commons.  Videos: YouTube (yt-dlp).  Voz: gTTS / voz del PC.
Ejecutar main.py (botón ▶ de VS Code) abre la ventana "IA".
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
SALIDA = CARPETA / "salida"
ARCHIVO_CLAVE = CARPETA / "clave.txt"
UA = {"User-Agent": "IA-Escolar/3.0 (proyecto educativo; python-urllib)"}

MODELO_CLAUDE = os.getenv("MODELO_CLAUDE", "claude-sonnet-5-5")
MODELO_GEMINI = os.getenv("MODELO_GEMINI", "")      # vacío = se elige solo
MODELO_OLLAMA = os.getenv("MODELO_OLLAMA", "")      # vacío = se elige solo


def _url_ollama() -> str:
    base = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").strip().rstrip("/")
    return base if base.startswith("http") else "http://" + base


INSTRUCCIONES = (
    "Eres una IA asistente que habla español y explica como un buen profesor. "
    "Reglas: "
    "1) Responde DIRECTAMENTE lo que se pregunta, sin cambiar de tema ni dar rodeos. "
    "2) Explica con claridad y precisión en 80 a 160 palabras y, cuando ayude, incluye "
    "un ejemplo concreto (empieza ese ejemplo con 'Por ejemplo,'). "
    "3) Escribe texto plano pensado para leerse en voz alta: sin markdown, sin "
    "asteriscos, sin viñetas, sin emojis y sin direcciones web. "
    "4) Si no estás seguro o no lo sabes, dilo con honestidad; nunca inventes datos. "
    "5) Si la pregunta continúa la conversación, usa el contexto anterior. "
    "Tu salida debe tener EXACTAMENTE estas tres partes, cada una en su línea:\n"
    "RESPUESTA: <tu respuesta>\n"
    "FOTOS: <2 a 4 palabras para buscar fotos reales de lo preguntado>\n"
    "VIDEOS: <3 a 6 palabras para buscar en YouTube un video educativo de lo preguntado>"
)

# Base local opcional: (palabras que TODAS deben aparecer, respuesta, tema).
BASE_LOCAL: list[tuple[set[str], str, str]] = [
    ({"paramos", "pais"},
     "Colombia es el país con más páramos del mundo: alberga cerca de la mitad "
     "de los páramos del planeta, entre ellos Sumapaz, Chingaza y Santurbán. "
     "Los páramos captan y almacenan agua, por eso son tan importantes.",
     "Páramo Colombia"),
    ({"capital", "colombia"},
     "La capital de Colombia es Bogotá, situada a unos 2.600 metros sobre el nivel del mar.",
     "Bogotá"),
]

PALABRAS_VACIAS = {
    "cual", "cuales", "que", "quien", "quienes", "como", "donde", "cuando", "cuanto",
    "cuantos", "es", "son", "fue", "era", "el", "la", "los", "las", "un", "una", "unos",
    "unas", "de", "del", "al", "en", "y", "o", "a", "por", "para", "con", "me", "te",
    "se", "dime", "puedes", "explica", "explicame", "hablame", "sobre", "acerca",
    "quiero", "saber", "tiene", "hay", "mi", "su", "lo",
}


def _norm(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def palabras_clave(pregunta: str) -> list[str]:
    return [p for p in re.findall(r"[a-z0-9]+", _norm(pregunta))
            if p not in PALABRAS_VACIAS and len(p) > 1]


def _http(url: str, timeout: int = 12) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _http_json(url: str, timeout: int = 12, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _post_json(url: str, payload: dict, headers: dict | None = None,
               timeout: int = 90) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={**UA, "Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"HTTP {e.code}: {detalle}") from e


@dataclass
class Respuesta:
    texto: str
    tema: str                  # tema general (respaldo)
    fuente: str                # qué motor respondió
    fotos: str = ""            # consulta para fotos
    videos: str = ""           # consulta para videos

    @property
    def consulta_fotos(self) -> str:
        return self.fotos or self.tema

    @property
    def consulta_videos(self) -> str:
        return self.videos or self.tema


@dataclass
class Foto:
    titulo: str
    pagina: str
    datos: bytes = b""


@dataclass
class Video:
    titulo: str
    canal: str
    duracion: str
    url: str
    datos: bytes = b""


def _sin_markdown(texto: str) -> str:
    texto = re.sub(r"[*`]", "", texto)
    texto = re.sub(r"^\s*#+\s*", "", texto, flags=re.M)
    texto = re.sub(r"^\s*[-•]\s+", "", texto, flags=re.M)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def parsear_salida(bruto: str, pregunta: str) -> Respuesta | None:
    """Separa RESPUESTA / FOTOS / VIDEOS de lo que devolvió el modelo."""
    bruto = (bruto or "").strip()
    if not bruto:
        return None

    def campo(nombre: str) -> str:
        m = re.search(
            rf"^\s*\**{nombre}\**\s*:\s*(.+?)(?=^\s*\**(?:RESPUESTA|FOTOS|VIDEOS)\**\s*:|\Z)",
            bruto, re.M | re.S | re.I)
        return m.group(1).strip() if m else ""

    texto = campo("RESPUESTA")
    if not texto:   # el modelo ignoró el formato: usamos todo menos las líneas de etiqueta
        texto = re.sub(r"^\s*\**(FOTOS|VIDEOS)\**\s*:.*$", "", bruto,
                       flags=re.M | re.I)
        texto = re.sub(r"^\s*\**RESPUESTA\**\s*:\s*", "", texto, flags=re.I)
    texto = _sin_markdown(texto)
    if not texto:
        return None
    tema = " ".join(palabras_clave(pregunta)[:3])
    fotos = _sin_markdown(campo("FOTOS")).splitlines()[0] if campo("FOTOS") else ""
    videos = _sin_markdown(campo("VIDEOS")).splitlines()[0] if campo("VIDEOS") else ""
    return Respuesta(texto, tema, "", fotos or tema, videos or tema)


class IAGenerativa:
    def __init__(self, idioma: str = "es"):
        self.idioma = idioma
        self.historial: list[dict] = []     # memoria de la conversación
        self._modelo_gemini_ok = ""
        SALIDA.mkdir(exist_ok=True)

    # ================================================== CLAVES Y MOTORES
    @staticmethod
    def leer_claves() -> list[tuple[str, str]]:
        """Claves disponibles como (tipo, clave). Lee variables de entorno y clave.txt."""
        claves: list[tuple[str, str]] = []
        for tipo, var in (("claude", "ANTHROPIC_API_KEY"), ("gemini", "GEMINI_API_KEY"),
                          ("gemini", "GOOGLE_API_KEY")):
            v = os.getenv(var, "").strip()
            if v:
                claves.append((tipo, v))
        if ARCHIVO_CLAVE.exists():
            for linea in ARCHIVO_CLAVE.read_text(encoding="utf-8-sig").splitlines():
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                linea = linea.split("=", 1)[-1].strip().strip("\"'")
                if linea:
                    claves.append(("gemini" if linea.startswith("AIza") else "claude", linea))
        return claves

    @staticmethod
    def guardar_clave(clave: str) -> None:
        clave = clave.strip()
        if clave:
            ARCHIVO_CLAVE.write_text(clave + "\n", encoding="utf-8")
        elif ARCHIVO_CLAVE.exists():
            ARCHIVO_CLAVE.unlink()

    def _modelos_ollama(self) -> list[str]:
        try:
            datos = _http_json(_url_ollama() + "/api/tags", timeout=2)
        except Exception:  # noqa: BLE001
            return []
        return [m["name"] for m in datos.get("models", [])
                if "embed" not in m.get("name", "").lower()]

    def _elegir_ollama(self) -> str | None:
        modelos = self._modelos_ollama()
        if not modelos:
            return None
        if MODELO_OLLAMA:
            return MODELO_OLLAMA
        for pref in ("llama3", "qwen", "gemma", "mistral", "phi"):
            for m in modelos:
                if pref in m.lower():
                    return m
        return modelos[0]

    def motores(self) -> list[tuple[str, object]]:
        """Motores de razonamiento disponibles ahora, en orden de preferencia."""
        lista: list[tuple[str, object]] = []
        for tipo, clave in self.leer_claves():
            if tipo == "claude":
                lista.append(("Claude", lambda msgs, k=clave: self._claude(k, msgs)))
            else:
                lista.append(("Gemini", lambda msgs, k=clave: self._gemini(k, msgs)))
        modelo = self._elegir_ollama()
        if modelo:
            lista.append((f"Ollama ({modelo})", lambda msgs, m=modelo: self._ollama(m, msgs)))
        return lista

    def describir_motor(self) -> str:
        propios = self.motores()
        return propios[0][0] if propios else "IA gratuita en línea (sin clave)"

    # ---- IA gratuita sin clave (servicio de terceros; puede tener límites)
    def _gratuita(self, mensajes: list[dict]) -> str:
        errores: list[str] = []
        for url in ("https://text.pollinations.ai/openai",
                    "https://gen.pollinations.ai/v1/chat/completions"):
            try:
                r = _post_json(
                    url,
                    {"model": "openai", "temperature": 0.3,
                     "messages": [{"role": "system", "content": INSTRUCCIONES}] + mensajes},
                    timeout=60)
                texto = r["choices"][0]["message"]["content"]
                if texto and texto.strip():
                    return texto
                errores.append("respuesta vacía")
            except Exception as e:  # noqa: BLE001
                errores.append(str(e)[:120])
        raise RuntimeError("; ".join(errores))

    # ---- Claude
    def _claude(self, clave: str, mensajes: list[dict]) -> str:
        r = _post_json(
            "https://api.anthropic.com/v1/messages",
            {"model": MODELO_CLAUDE, "max_tokens": 800, "system": INSTRUCCIONES,
             "messages": mensajes},
            {"x-api-key": clave, "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in r.get("content", [])
                       if b.get("type") == "text")

    # ---- Gemini
    def _modelos_gemini(self, clave: str) -> list[str]:
        if MODELO_GEMINI:
            return [MODELO_GEMINI]
        if self._modelo_gemini_ok:
            return [self._modelo_gemini_ok]
        candidatos: list[str] = []
        try:
            datos = _http_json("https://generativelanguage.googleapis.com/v1beta/models"
                               "?pageSize=200", headers={"x-goog-api-key": clave})
            malos = ("lite", "image", "tts", "live", "audio", "exp", "vision",
                     "embed", "preview", "thinking", "robotics", "computer")
            for m in datos.get("models", []):
                nombre = m.get("name", "").replace("models/", "")
                if ("generateContent" in m.get("supportedGenerationMethods", [])
                        and "flash" in nombre and not any(x in nombre for x in malos)):
                    candidatos.append(nombre)
        except Exception:  # noqa: BLE001
            pass
        candidatos.sort(reverse=True)           # versiones más nuevas primero
        return (candidatos[:3] or []) + ["gemini-2.5-flash", "gemini-2.0-flash"]

    def _gemini(self, clave: str, mensajes: list[dict]) -> str:
        contenidos = [{"role": "user" if m["role"] == "user" else "model",
                       "parts": [{"text": m["content"]}]} for m in mensajes]
        errores: list[str] = []
        for modelo in self._modelos_gemini(clave):
            try:
                r = _post_json(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                    {"systemInstruction": {"parts": [{"text": INSTRUCCIONES}]},
                     "contents": contenidos,
                     "generationConfig": {"temperature": 0.3, "maxOutputTokens": 900}},
                    {"x-goog-api-key": clave})
                partes = r["candidates"][0]["content"]["parts"]
                texto = "".join(p.get("text", "") for p in partes)
                if texto.strip():
                    self._modelo_gemini_ok = modelo
                    return texto
                errores.append(f"{modelo}: respuesta vacía")
            except Exception as e:  # noqa: BLE001
                errores.append(f"{modelo}: {e}")
                if "API key" in str(e) or "HTTP 400" in str(e) or "HTTP 403" in str(e):
                    break           # clave mala: probar otros modelos no sirve
        raise RuntimeError("; ".join(errores))

    # ---- Ollama
    def _ollama(self, modelo: str, mensajes: list[dict]) -> str:
        r = _post_json(
            _url_ollama() + "/api/chat",
            {"model": modelo, "stream": False,
             "messages": [{"role": "system", "content": INSTRUCCIONES}] + mensajes,
             "options": {"temperature": 0.3, "num_predict": 700}},
            timeout=240)
        return r["message"]["content"]

    # ================================================== TEXTO
    def _mensajes(self, pregunta: str) -> list[dict]:
        return self.historial[-6:] + [{"role": "user", "content": pregunta}]

    def _recordar(self, pregunta: str, respuesta: str) -> None:
        self.historial += [{"role": "user", "content": pregunta},
                           {"role": "assistant", "content": respuesta}]
        self.historial = self.historial[-8:]

    def responder_texto(self, pregunta: str) -> Respuesta:
        propios = self.motores()          # con clave o Ollama: los que tú configuraste
        motores = propios + [("IA gratuita", self._gratuita)]
        errores: list[str] = []
        for nombre, funcion in motores:
            try:
                resp = parsear_salida(funcion(self._mensajes(pregunta)), pregunta)
            except Exception as e:  # noqa: BLE001
                errores.append(f"{nombre}: {e}")
                print(f"[IA] {nombre} falló: {e}")
                continue
            if resp:
                resp.fuente = nombre
                self._recordar(pregunta, resp.texto)
                return resp
            errores.append(f"{nombre}: respuesta vacía")
        if propios:     # había IA configurada pero falló: error claro, no respuestas absurdas
            return Respuesta(
                "No pude obtener la respuesta de la IA. " + " | ".join(errores)[:400] +
                " Revisa tu internet y tu clave (botón 🔑 Clave).", "", "Error")
        return self._responder_basico(pregunta)

    # ---- modo básico (sin IA): honesto sobre sus límites
    def _responder_basico(self, pregunta: str) -> Respuesta:
        local = self._buscar_local(pregunta)
        if local:
            return local
        try:
            wiki = self._buscar_wikipedia(pregunta)
        except Exception:  # noqa: BLE001
            return Respuesta("No pude consultar internet. Revisa tu conexión.", "", "Sin conexión")
        if wiki:
            return wiki
        return Respuesta(
            "No pude conectar con la IA en línea y en Wikipedia no hay un artículo que "
            "responda eso. Revisa tu internet e inténtalo de nuevo. Si sigue fallando, "
            "pulsa 🔑 Clave y pega una clave gratuita de Google Gemini.", "", "Sin resultados")

    def _buscar_local(self, pregunta: str) -> Respuesta | None:
        palabras = set(re.findall(r"[a-z0-9]+", _norm(pregunta)))

        def coincide(k: str) -> bool:
            return any(p == k or (len(k) >= 5 and p[:5] == k[:5]) for p in palabras)

        for claves, texto, tema in BASE_LOCAL:
            if all(coincide(k) for k in claves):
                return Respuesta(texto, tema, "Base local", tema, tema)
        return None

    @staticmethod
    def _limpiar_extracto(extracto: str, max_frases: int = 4, max_chars: int = 650) -> str:
        extracto = re.sub(r"\s*\([^)]*\)", "", extracto)
        extracto = re.sub(r"\s*\[[^\]]*\]", "", extracto)
        extracto = re.sub(r"\s+", " ", extracto).strip()
        frases = re.split(r"(?<=[.!?])\s+", extracto)
        salida: list[str] = []
        for f in frases[:max_frases]:
            if salida and len(" ".join(salida + [f])) > max_chars:
                break
            salida.append(f)
        return " ".join(salida)

    @staticmethod
    def _elegir_pagina(paginas: dict, claves: list[str]) -> dict | None:
        mejor, mejor_puntos = None, -1e9
        for p in paginas.values():
            extracto = (p.get("extract") or "").strip()
            if not extracto or "puede referirse a" in extracto[:300].lower():
                continue
            titulo, cuerpo = _norm(p.get("title", "")), _norm(extracto)
            raices = [k[:-1] if len(k) > 3 and k.endswith("s") else k for k in claves]
            en_titulo = sum(k in titulo for k in raices)
            en_cuerpo = sum(k in cuerpo for k in raices)
            relevante = en_titulo >= 1 or (len(claves) >= 2 and en_cuerpo >= len(claves))
            if not relevante:       # evita artículos que no tienen nada que ver
                continue
            puntos = 3 * en_titulo + en_cuerpo - 0.3 * p.get("index", 9)
            if puntos > mejor_puntos:
                mejor, mejor_puntos = p, puntos
        return mejor

    def _buscar_wikipedia(self, pregunta: str) -> Respuesta | None:
        claves = palabras_clave(pregunta)
        if not claves:
            return None
        params = urllib.parse.urlencode({
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": " ".join(claves), "gsrlimit": 5, "prop": "extracts",
            "exintro": 1, "explaintext": 1, "exlimit": 5, "redirects": 1,
        })
        datos = _http_json(f"https://es.wikipedia.org/w/api.php?{params}")
        pagina = self._elegir_pagina(datos.get("query", {}).get("pages", {}), claves)
        if not pagina:
            return None
        extra = " ".join(k for k in claves if k not in _norm(pagina["title"]))[:40]
        return Respuesta(self._limpiar_extracto(pagina["extract"]), pagina["title"],
                         "Wikipedia (modo básico: resume, no razona)",
                         pagina["title"], f"{pagina['title']} {extra}".strip())

    # ================================================== FOTOS
    def buscar_fotos(self, tema: str, cantidad: int = 4) -> list[Foto]:
        if not tema:
            return []
        params = urllib.parse.urlencode({
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": f"{tema} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 20,
            "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": 480,
        })
        datos = _http_json(f"https://commons.wikimedia.org/w/api.php?{params}")
        paginas = sorted(datos.get("query", {}).get("pages", {}).values(),
                         key=lambda p: p.get("index", 99))
        candidatas: list[Foto] = []
        urls: list[str] = []
        for p in paginas:
            info = (p.get("imageinfo") or [{}])[0]
            if info.get("mime") not in ("image/jpeg", "image/png"):
                continue
            miniatura = info.get("thumburl") or info.get("url")
            if not miniatura:
                continue
            titulo = re.sub(r"^Archivo:|^File:", "", p.get("title", "")).rsplit(".", 1)[0]
            candidatas.append(Foto(titulo, info.get("descriptionurl", "")))
            urls.append(miniatura)
            if len(candidatas) >= cantidad + 3:
                break

        def bajar(u: str) -> bytes:
            try:
                return _http(u)
            except Exception:  # noqa: BLE001
                return b""

        with ThreadPoolExecutor(max_workers=6) as pool:
            for foto, datos_foto in zip(candidatas, pool.map(bajar, urls)):
                foto.datos = datos_foto
        return [f for f in candidatas if f.datos][:cantidad]

    # ================================================== VIDEOS
    @staticmethod
    def _duracion(segundos) -> str:
        if not segundos:
            return ""
        s = int(segundos)
        h, resto = divmod(s, 3600)
        m, s = divmod(resto, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    def buscar_videos(self, tema: str, pregunta: str = "", cantidad: int = 3) -> list[Video]:
        if not tema:
            return []
        import yt_dlp

        extra = [k for k in palabras_clave(pregunta) if k not in _norm(tema)][:3]
        consulta = " ".join([tema] + extra)
        opciones = {"quiet": True, "no_warnings": True, "extract_flat": True,
                    "skip_download": True}
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(f"ytsearch{cantidad + 2}:{consulta}", download=False)
        videos: list[Video] = []
        for e in (info or {}).get("entries") or []:
            vid = e.get("id")
            if not vid:
                continue
            videos.append(Video(
                titulo=e.get("title") or "Video",
                canal=e.get("channel") or e.get("uploader") or "",
                duracion=self._duracion(e.get("duration")),
                url=e.get("url") if str(e.get("url", "")).startswith("http")
                else f"https://www.youtube.com/watch?v={vid}",
            ))
            if len(videos) >= cantidad:
                break

        def miniatura(v: Video) -> bytes:
            vid = v.url.split("v=")[-1].split("&")[0]
            try:
                return _http(f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg")
            except Exception:  # noqa: BLE001
                return b""

        with ThreadPoolExecutor(max_workers=4) as pool:
            for v, d in zip(videos, pool.map(miniatura, videos)):
                v.datos = d
        return videos

    # ================================================== VOZ
    def hablar(self, texto: str, nombre: str = "voz") -> Path:
        """Convierte el texto en audio y devuelve el archivo (para reproducirlo)."""
        SALIDA.mkdir(exist_ok=True)
        texto = texto[:1800]
        ruta = SALIDA / f"{nombre}.mp3"
        try:
            from gtts import gTTS

            gTTS(text=texto, lang=self.idioma).save(str(ruta))
            return ruta
        except Exception as e_online:  # noqa: BLE001
            ruta.unlink(missing_ok=True)
            try:  # respaldo sin internet
                import pyttsx3

                ruta = SALIDA / f"{nombre}.wav"
                motor = pyttsx3.init()
                motor.save_to_file(texto, str(ruta))
                motor.runAndWait()
                return ruta
            except Exception as e_offline:  # noqa: BLE001
                raise RuntimeError(
                    f"No pude generar la voz (gTTS: {e_online}; local: {e_offline})"
                ) from e_offline

    def hablar_local(self, texto: str) -> None:
        """Dice el texto con la voz del computador (Windows: voces de Microsoft)."""
        try:                                    # Windows necesita esto en hilos secundarios
            import comtypes
            comtypes.CoInitialize()
        except Exception:  # noqa: BLE001
            pass
        import pyttsx3

        motor = pyttsx3.init()
        for voz in motor.getProperty("voices") or []:
            etiqueta = f"{voz.name} {voz.id} {getattr(voz, 'languages', '')}".lower()
            if any(p in etiqueta for p in ("spanish", "español", "es-", "es_", "helena",
                                           "sabina", "pablo", "raul", "laura")):
                motor.setProperty("voice", voz.id)
                break
        motor.setProperty("rate", 175)
        motor.say(texto[:1800])
        motor.runAndWait()


if __name__ == "__main__":      # botón ▶ de VS Code sobre este archivo
    import main

    main.iniciar()