"""Ventana "IA": pregunta lo que quieras y responde con texto, voz, fotos y videos.

Pulsa el botón ▶ de VS Code sobre este archivo (o ejecuta: python main.py).
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from itertools import count
from pathlib import Path

# --- Instala solo lo que falte, para que baste con pulsar ▶ ----------------
_LIBRERIAS = [("PySide6", "PySide6", True), ("gtts", "gTTS", True),
              ("yt_dlp", "yt-dlp", True), ("pyttsx3", "pyttsx3", False)]


def asegurar_librerias() -> None:
    for modulo, paquete, obligatoria in _LIBRERIAS:
        if importlib.util.find_spec(modulo) is not None:
            continue
        print(f"Instalando {paquete} (solo la primera vez)...", flush=True)
        r = subprocess.run([sys.executable, "-m", "pip", "install", paquete])
        if r.returncode != 0 and obligatoria:
            print(f"\nNo pude instalar {paquete}. Revisa tu internet y vuelve a "
                  f"pulsar ▶.", flush=True)
            sys.exit(1)


asegurar_librerias()

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QPainter, QPainterPath, QPixmap, QPolygonF
from PySide6.QtCore import QPointF
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QInputDialog, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from ia_generativa import IAGenerativa

ESTILO = """
* { font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif; font-size: 14px; }
QMainWindow, #raiz { background: #0e1218; }
#cabecera { background: #131a23; border-bottom: 1px solid #222c3a; }
#logo { color: #ffffff; font-size: 22px; font-weight: 700; }
#subtitulo { color: #8b98a9; font-size: 12px; }
QCheckBox { color: #c9d4e2; spacing: 8px; }
QScrollArea { border: none; background: transparent; }
#feed { background: transparent; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: #2a3546; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
#burbuja { background: #2f6bff; color: #ffffff; border-radius: 16px; padding: 11px 16px; }
#tarjeta { background: #161d27; border: 1px solid #222c3a; border-radius: 16px; }
#ia_titulo { color: #7fb0ff; font-weight: 700; font-size: 13px; }
#estado { color: #8b98a9; }
#texto { color: #e6edf3; font-size: 15px; }
#fuente { color: #6f7d90; font-size: 11px; }
#seccion { color: #c9d4e2; font-weight: 600; font-size: 13px; }
#nota { color: #8b98a9; font-size: 12px; }
#video_titulo { color: #e6edf3; font-size: 12px; }
#video_canal { color: #8b98a9; font-size: 11px; }
#bienvenida { color: #ffffff; font-size: 28px; font-weight: 700; }
#bienvenida_sub { color: #8b98a9; font-size: 14px; }
QPushButton#chip { background: #161d27; color: #c9d4e2; border: 1px solid #2a3546;
                   border-radius: 16px; padding: 9px 16px; }
QPushButton#chip:hover { background: #1d2733; border-color: #3b6bd6; color: #ffffff; }
QPushButton#detener { background: #1d2733; color: #c9d4e2; border: 1px solid #2a3546;
                      border-radius: 14px; padding: 6px 14px; }
QPushButton#detener:hover { background: #26323f; }
#barra { background: #131a23; border-top: 1px solid #222c3a; }
QLineEdit { background: #0e1218; color: #ffffff; border: 1px solid #2a3546;
            border-radius: 22px; padding: 12px 20px; font-size: 15px; }
QLineEdit:focus { border-color: #3b7bff; }
QPushButton#enviar { background: #2f6bff; color: #ffffff; border: none; border-radius: 22px;
                     padding: 12px 26px; font-weight: 600; font-size: 15px; }
QPushButton#enviar:hover { background: #4a80ff; }
QPushButton#enviar:disabled { background: #25324a; color: #6f7d90; }
"""

ANCHO_FOTO, ALTO_FOTO = 196, 138
ANCHO_VIDEO, ALTO_VIDEO = 262, 147

SUGERENCIAS = [
    "¿Cuál es el país que más páramos tiene en el mundo?",
    "¿Qué es la fotosíntesis?",
    "Machu Picchu",
    "¿Cómo funciona un avión?",
]


# ------------------------------------------------------------- utilidades
def pixmap_redondeado(datos: bytes, ancho: int, alto: int, radio: int = 12,
                      reproducir: bool = False, duracion: str = "") -> QPixmap | None:
    pm = QPixmap()
    if not datos or not pm.loadFromData(datos):
        return None
    pm = pm.scaled(ancho, alto, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    pm = pm.copy((pm.width() - ancho) // 2, (pm.height() - alto) // 2, ancho, alto)
    salida = QPixmap(ancho, alto)
    salida.fill(Qt.transparent)
    p = QPainter(salida)
    p.setRenderHint(QPainter.Antialiasing)
    ruta = QPainterPath()
    ruta.addRoundedRect(0, 0, ancho, alto, radio, radio)
    p.setClipPath(ruta)
    p.drawPixmap(0, 0, pm)
    if reproducir:                                   # botón ▶ encima de la miniatura
        p.setBrush(Qt.black)
        p.setOpacity(0.55)
        p.setPen(Qt.NoPen)
        cx, cy = ancho / 2, alto / 2
        p.drawEllipse(QPointF(cx, cy), 26, 26)
        p.setOpacity(1.0)
        p.setBrush(Qt.white)
        p.drawPolygon(QPolygonF([QPointF(cx - 8, cy - 12), QPointF(cx - 8, cy + 12),
                                 QPointF(cx + 14, cy)]))
        if duracion:
            p.setOpacity(0.8)
            p.setBrush(Qt.black)
            p.drawRoundedRect(ancho - 58, alto - 26, 50, 18, 5, 5)
            p.setOpacity(1.0)
            p.setPen(Qt.white)
            p.drawText(ancho - 58, alto - 26, 50, 18, Qt.AlignCenter, duracion)
    p.end()
    return salida


def abrir_enlace(url: str) -> None:
    if url:
        QDesktopServices.openUrl(QUrl(url))


class Clicable(QFrame):
    clicado = Signal()

    def __init__(self):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):  # noqa: N802
        if e.button() == Qt.LeftButton:
            self.clicado.emit()


class Senales(QObject):
    listo = Signal(object)
    fallo = Signal(str)


class Tarea(QRunnable):
    """Ejecuta una función en segundo plano para que la ventana no se congele."""

    def __init__(self, fn, *args):
        super().__init__()
        self.setAutoDelete(False)
        self.fn, self.args = fn, args
        self.senales = Senales()

    def run(self):
        try:
            resultado = self.fn(*self.args)
        except Exception as e:  # noqa: BLE001
            try:
                self.senales.fallo.emit(str(e))
            except RuntimeError:    # la ventana ya se cerró: no hay a quién avisar
                pass
            return
        try:
            self.senales.listo.emit(resultado)
        except RuntimeError:        # la ventana ya se cerró
            pass


# ------------------------------------------------------------- bloque de chat
class Bloque(QWidget):
    cambio = Signal()
    repetir = Signal()

    def __init__(self, pregunta: str):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        fila = QHBoxLayout()
        fila.addStretch()
        burbuja = QLabel(pregunta)
        burbuja.setObjectName("burbuja")
        burbuja.setWordWrap(True)
        burbuja.setMaximumWidth(640)
        fila.addWidget(burbuja)
        lay.addLayout(fila)

        self.tarjeta = QFrame()
        self.tarjeta.setObjectName("tarjeta")
        tl = QVBoxLayout(self.tarjeta)
        tl.setContentsMargins(20, 16, 20, 18)
        tl.setSpacing(10)
        titulo = QLabel("✦  IA")
        titulo.setObjectName("ia_titulo")
        tl.addWidget(titulo)

        self.estado = QLabel("Pensando")
        self.estado.setObjectName("estado")
        tl.addWidget(self.estado)

        self.texto = QLabel()
        self.texto.setObjectName("texto")
        self.texto.setWordWrap(True)
        self.texto.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.texto.hide()
        tl.addWidget(self.texto)

        self.fuente = QLabel()
        self.fuente.setObjectName("fuente")
        self.fuente.hide()
        tl.addWidget(self.fuente)
        self._fuente_base = ""

        self.boton_voz = QPushButton("🔊  Escuchar")
        self.boton_voz.setObjectName("detener")
        self.boton_voz.setCursor(Qt.PointingHandCursor)
        self.boton_voz.clicked.connect(self.repetir.emit)
        self.boton_voz.hide()
        fila_voz = QHBoxLayout()
        fila_voz.addWidget(self.boton_voz)
        fila_voz.addStretch()
        tl.addLayout(fila_voz)

        self.sec_fotos, self.fila_fotos = self._seccion("Imágenes", tl)
        self.sec_videos, self.fila_videos = self._seccion("Videos", tl)
        lay.addWidget(self.tarjeta)

        self._puntos = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animar)
        self._timer.start(400)

    def _seccion(self, nombre: str, padre: QVBoxLayout):
        cont = QWidget()
        v = QVBoxLayout(cont)
        v.setContentsMargins(0, 6, 0, 0)
        v.setSpacing(8)
        etiqueta = QLabel(nombre)
        etiqueta.setObjectName("seccion")
        v.addWidget(etiqueta)
        fila = QHBoxLayout()
        fila.setSpacing(12)
        v.addLayout(fila)
        cont.hide()
        padre.addWidget(cont)
        return cont, fila

    def _animar(self):
        self._puntos = (self._puntos + 1) % 4
        self.estado.setText("Pensando" + "." * self._puntos)

    def _quitar_estado(self):
        self._timer.stop()
        self.estado.hide()

    # ---- contenido
    def set_texto(self, texto: str, fuente: str):
        self._quitar_estado()
        self.texto.setText(texto)
        self.texto.show()
        self._fuente_base = f"Fuente: {fuente}"
        self.fuente.setText(self._fuente_base)
        self.fuente.show()
        if fuente not in ("Sin conexión", "Sin resultados", "Error"):
            self.boton_voz.show()
        self.cambio.emit()

    def aviso_voz(self, mensaje: str):
        self.fuente.setText(f"{self._fuente_base}  ·  {mensaje}")

    def set_error(self, mensaje: str):
        self._quitar_estado()
        self.texto.setText(mensaje)
        self.texto.show()
        self.cambio.emit()

    def set_fotos(self, fotos):
        if not fotos:
            return self.nota(self.sec_fotos, self.fila_fotos, "No encontré imágenes de este tema.")
        for f in fotos:
            pm = pixmap_redondeado(f.datos, ANCHO_FOTO, ALTO_FOTO)
            if not pm:
                continue
            tarjeta = Clicable()
            v = QVBoxLayout(tarjeta)
            v.setContentsMargins(0, 0, 0, 0)
            img = QLabel()
            img.setPixmap(pm)
            v.addWidget(img)
            tarjeta.setToolTip(f.titulo)
            tarjeta.clicado.connect(lambda url=f.pagina: abrir_enlace(url))
            self.fila_fotos.addWidget(tarjeta)
        self.fila_fotos.addStretch()
        self.sec_fotos.show()
        self.cambio.emit()

    def set_videos(self, videos):
        if not videos:
            return self.nota(self.sec_videos, self.fila_videos, "No encontré videos de este tema.")
        for vd in videos:
            tarjeta = Clicable()
            v = QVBoxLayout(tarjeta)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(5)
            miniatura = QLabel()
            pm = pixmap_redondeado(vd.datos, ANCHO_VIDEO, ALTO_VIDEO,
                                   reproducir=True, duracion=vd.duracion)
            if pm:
                miniatura.setPixmap(pm)
            else:
                miniatura.setFixedSize(ANCHO_VIDEO, ALTO_VIDEO)
                miniatura.setStyleSheet("background:#222c3a;border-radius:12px;")
            v.addWidget(miniatura)
            titulo = QLabel(vd.titulo if len(vd.titulo) < 62 else vd.titulo[:60] + "…")
            titulo.setObjectName("video_titulo")
            titulo.setWordWrap(True)
            titulo.setFixedWidth(ANCHO_VIDEO)
            v.addWidget(titulo)
            canal = QLabel(vd.canal)
            canal.setObjectName("video_canal")
            v.addWidget(canal)
            v.addStretch()
            tarjeta.setToolTip(vd.titulo)
            tarjeta.clicado.connect(lambda url=vd.url: abrir_enlace(url))
            self.fila_videos.addWidget(tarjeta)
        self.fila_videos.addStretch()
        self.sec_videos.show()
        self.cambio.emit()

    def nota(self, seccion, fila, mensaje: str):
        n = QLabel(mensaje)
        n.setObjectName("nota")
        fila.addWidget(n)
        seccion.show()
        self.cambio.emit()


# ------------------------------------------------------------- orquestación
class Consulta(QObject):
    """Una pregunta: texto -> (voz, fotos, videos) en paralelo."""

    def __init__(self, ventana: "Ventana", pregunta: str, bloque: Bloque, numero: int):
        super().__init__(ventana)
        self.v, self.pregunta, self.bloque, self.n = ventana, pregunta, bloque, numero
        self.tema = ""
        self.texto_resp = ""
        self.ruta_voz = None
        self.bloque.repetir.connect(self._repetir)

    def iniciar(self):
        self._lanzar(self.v.ia.responder_texto, self._texto, self._error_texto, self.pregunta)

    def _lanzar(self, fn, ok, fallo, *args):
        t = Tarea(fn, *args)
        t.senales.listo.connect(ok)
        t.senales.fallo.connect(fallo)
        self.v.tareas.append(t)
        self.v.pool.start(t)

    def _texto(self, resp):
        self.tema = resp.tema
        self.texto_resp = resp.texto
        self.bloque.set_texto(resp.texto, resp.fuente)
        self.v.habilitar_entrada()
        if self.v.voz_activa() and resp.fuente not in ("Sin conexión", "Sin resultados",
                                                       "Error"):
            self._lanzar(self.v.ia.hablar, self._voz, self._error_voz,
                         resp.texto, f"voz_{self.n}")
        if resp.fuente != "Error" and resp.consulta_fotos:
            self._lanzar(self.v.ia.buscar_fotos, self.bloque.set_fotos, self._error_fotos,
                         resp.consulta_fotos)
            self._lanzar(self.v.ia.buscar_videos, self.bloque.set_videos, self._error_videos,
                         resp.consulta_videos)

    def _error_texto(self, msg):
        self.bloque.set_error(f"Ocurrió un problema: {msg}")
        self.v.habilitar_entrada()

    def _voz(self, ruta):
        self.ruta_voz = ruta
        self.v.reproducir(ruta, self.texto_resp)

    def _error_voz(self, msg):
        print("[voz]", msg)
        self.bloque.aviso_voz("usando la voz del equipo")
        self.v.voz_local(self.texto_resp, msg)

    def _repetir(self):
        if not self.texto_resp:
            return
        if self.ruta_voz:
            self.v.reproducir(self.ruta_voz, self.texto_resp)
        else:
            self._lanzar(self.v.ia.hablar, self._voz, self._error_voz,
                         self.texto_resp, f"voz_{self.n}")

    def _error_fotos(self, msg):
        self.bloque.nota(self.bloque.sec_fotos, self.bloque.fila_fotos,
                         "No se pudieron cargar las imágenes (revisa tu internet).")

    def _error_videos(self, msg):
        self.bloque.nota(self.bloque.sec_videos, self.bloque.fila_videos,
                         "No se pudieron cargar los videos (revisa tu internet "
                         "o instala yt-dlp).")


# ------------------------------------------------------------- ventana
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IA")
        self.resize(1040, 780)
        self.setMinimumSize(980, 560)
        self.ia = IAGenerativa()
        self.pool = QThreadPool.globalInstance()
        self.tareas: list[Tarea] = []
        self.consultas: list[Consulta] = []
        self._numero = count(1)

        self.audio = None          # se crean al hablar por primera vez, así la
        self.reproductor = None    # ventana abre siempre, aunque falle el audio

        raiz = QWidget()
        raiz.setObjectName("raiz")
        self.setCentralWidget(raiz)
        principal = QVBoxLayout(raiz)
        principal.setContentsMargins(0, 0, 0, 0)
        principal.setSpacing(0)

        # cabecera
        cab = QFrame()
        cab.setObjectName("cabecera")
        cl = QHBoxLayout(cab)
        cl.setContentsMargins(26, 14, 26, 14)
        textos = QVBoxLayout()
        textos.setSpacing(0)
        logo = QLabel("✦  IA")
        logo.setObjectName("logo")
        self.sub = QLabel()
        self.sub.setObjectName("subtitulo")
        sub = self.sub
        textos.addWidget(logo)
        textos.addWidget(sub)
        cl.addLayout(textos)
        cl.addStretch()
        self.chk_voz = QCheckBox("Leer la respuesta en voz alta")
        self.chk_voz.setChecked(True)
        cl.addWidget(self.chk_voz)
        detener = QPushButton("■  Detener voz")
        detener.setObjectName("detener")
        detener.setCursor(Qt.PointingHandCursor)
        detener.clicked.connect(self.detener_voz)
        cl.addSpacing(10)
        cl.addWidget(detener)
        boton_clave = QPushButton("🔑  Clave")
        boton_clave.setObjectName("detener")
        boton_clave.setCursor(Qt.PointingHandCursor)
        boton_clave.clicked.connect(self.pedir_clave)
        cl.addWidget(boton_clave)
        principal.addWidget(cab)

        # zona de conversación
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.feed = QWidget()
        self.feed.setObjectName("feed")
        self.feed_lay = QVBoxLayout(self.feed)
        self.feed_lay.setContentsMargins(34, 26, 34, 26)
        self.feed_lay.setSpacing(26)
        self.feed_lay.addStretch()
        self.scroll.setWidget(self.feed)
        principal.addWidget(self.scroll, 1)
        self._bienvenida()

        # barra de entrada
        barra = QFrame()
        barra.setObjectName("barra")
        bl = QHBoxLayout(barra)
        bl.setContentsMargins(26, 14, 26, 16)
        bl.setSpacing(12)
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Pregúntale lo que quieras a la IA…")
        self.entrada.returnPressed.connect(self.enviar)
        bl.addWidget(self.entrada, 1)
        self.boton = QPushButton("Enviar  ➤")
        self.boton.setObjectName("enviar")
        self.boton.setCursor(Qt.PointingHandCursor)
        self.boton.clicked.connect(self.enviar)
        bl.addWidget(self.boton)
        principal.addWidget(barra)
        self.entrada.setFocus()
        self.actualizar_motor()

    def actualizar_motor(self):
        self.sub.setText("Respuestas con texto, voz, imágenes y videos  ·  "
                         "Motor: " + self.ia.describir_motor())

    def pedir_clave(self):
        texto, ok = QInputDialog.getText(
            self, "Conectar la IA",
            "OPCIONAL. La IA ya funciona sola. Si quieres respuestas más rápidas y\n"
            "estables, pega aquí una\n"
            "clave GRATIS de Google Gemini (se crea en 1 minuto en\n"
            "aistudio.google.com/apikey) o una clave de Claude.\n\n"
            "Déjalo vacío para seguir con la IA gratuita sin clave.",
            QLineEdit.Normal, "")
        if ok:
            self.ia.guardar_clave(texto)
            self.actualizar_motor()

    # ---- bienvenida
    def _bienvenida(self):
        self.bienvenida = QWidget()
        v = QVBoxLayout(self.bienvenida)
        v.setAlignment(Qt.AlignHCenter)
        v.setSpacing(10)
        t = QLabel("¿En qué te puedo ayudar?")
        t.setObjectName("bienvenida")
        t.setAlignment(Qt.AlignCenter)
        s = QLabel("Pregunta algo y te respondo con texto, voz, imágenes y videos del tema.")
        s.setObjectName("bienvenida_sub")
        s.setAlignment(Qt.AlignCenter)
        v.addSpacing(40)
        v.addWidget(t)
        v.addWidget(s)
        v.addSpacing(18)
        for sugerencia in SUGERENCIAS:
            chip = QPushButton(sugerencia)
            chip.setObjectName("chip")
            chip.setCursor(Qt.PointingHandCursor)
            chip.clicked.connect(lambda _=False, q=sugerencia: self.enviar(q))
            fila = QHBoxLayout()
            fila.addStretch()
            fila.addWidget(chip)
            fila.addStretch()
            v.addLayout(fila)
        self.feed_lay.insertWidget(0, self.bienvenida)

    # ---- acciones
    def voz_activa(self) -> bool:
        return self.chk_voz.isChecked()

    def habilitar_entrada(self):
        self.boton.setEnabled(True)
        self.entrada.setEnabled(True)
        self.entrada.setFocus()

    def enviar(self, pregunta: str | None = None):
        if not isinstance(pregunta, str):
            pregunta = self.entrada.text()
        pregunta = pregunta.strip()
        if not pregunta or not self.boton.isEnabled():
            return
        self.detener_voz()
        self.bienvenida.hide()
        self.entrada.clear()
        self.boton.setEnabled(False)
        self.entrada.setEnabled(False)

        bloque = Bloque(pregunta)
        bloque.cambio.connect(self.ir_abajo)
        self.feed_lay.insertWidget(self.feed_lay.count() - 1, bloque)
        consulta = Consulta(self, pregunta, bloque, next(self._numero))
        self.consultas.append(consulta)
        consulta.iniciar()
        self.ir_abajo()

    def ir_abajo(self):
        QTimer.singleShot(60, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()))

    def closeEvent(self, evento):  # noqa: N802
        self.detener_voz()
        self.pool.clear()               # cancela lo que aún no empezó
        self.pool.waitForDone(1500)     # espera un poco a lo que está en curso
        super().closeEvent(evento)

    def detener_voz(self):
        if self.reproductor is not None:
            self.reproductor.stop()

    def reproducir(self, ruta, texto: str = ""):
        self.texto_voz = texto
        try:
            if self.reproductor is None:
                self.audio = QAudioOutput()
                self.audio.setVolume(1.0)
                self.reproductor = QMediaPlayer()
                self.reproductor.setAudioOutput(self.audio)
                self.reproductor.errorOccurred.connect(self._error_audio)
            self.reproductor.setSource(QUrl.fromLocalFile(str(ruta)))
            self.reproductor.play()
        except Exception as e:  # noqa: BLE001
            print("[audio] no se pudo reproducir:", e)
            self.voz_local(texto, str(e))

    def _error_audio(self, error, mensaje=""):
        print("[audio] error del reproductor:", error, mensaje)
        self.voz_local(getattr(self, "texto_voz", ""), mensaje)

    def voz_local(self, texto: str, motivo: str = ""):
        """Respaldo: la voz del propio computador (no necesita internet)."""
        if not texto:
            return
        print("[voz] usando la voz del computador. Motivo:", motivo)
        t = Tarea(self.ia.hablar_local, texto)
        t.senales.fallo.connect(lambda msg: print("[voz] la voz del equipo falló:", msg))
        self.tareas.append(t)
        self.pool.start(t)


def iniciar() -> None:
    print("Abriendo la IA...", flush=True)
    try:
        app = QApplication.instance() or QApplication(sys.argv)
        app.setStyleSheet(ESTILO)
        ventana = Ventana()
        # Se pone al frente (en Windows a veces abre detrás de VS Code)
        ventana.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        ventana.show()
        ventana.raise_()
        ventana.activateWindow()

        def quitar_al_frente():
            ventana.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            ventana.show()
            ventana.activateWindow()

        QTimer.singleShot(1200, quitar_al_frente)
        print("Ventana abierta. Si no la ves, búscala en la barra de tareas.", flush=True)
        codigo = app.exec()
    except Exception:  # noqa: BLE001
        import traceback

        detalle = traceback.format_exc()
        print("\nERROR AL ABRIR LA IA:\n" + detalle, flush=True)
        try:
            (Path(__file__).resolve().parent / "error.txt").write_text(detalle, encoding="utf-8")
        except OSError:
            pass
        input("\nPulsa Enter para cerrar...")
        sys.exit(1)
    sys.stdout.flush()
    os._exit(codigo)     # cierra del todo: así el siguiente ▶ siempre funciona


if __name__ == "__main__":
    iniciar()