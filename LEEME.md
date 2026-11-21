# IA (Punto 1: IA generativa)

Pregunta lo que quieras y responde con **texto**, **voz**, **imágenes** y **videos** del tema.

## Cómo abrirla
1. Archivo > Abrir carpeta (esta carpeta).
2. Abre `main.py` y pulsa el botón ▶. Nada más.

La primera vez instala sola las librerías que falten (tarda un par de minutos).
Después abre la ventana "IA" directo.

## Para que responda de verdad (importante)
Una IA que responde bien cualquier pregunta necesita un modelo de lenguaje.
Sin uno, solo puede resumir Wikipedia y por eso fallaba.

Al abrir, la ventana te pide una clave. Pega una de estas (sin usar la terminal):
- **Gemini (gratis):** entra a https://aistudio.google.com/apikey, crea la clave
  (empieza por `AIza`) y pégala.
- **Claude:** clave de Anthropic (empieza por `sk-ant-`).

Se guarda en `clave.txt`. El botón **🔑 Clave** de la cabecera sirve para cambiarla.
Arriba verás "Motor: ..." con lo que está usando.

Alternativa sin clave ni internet: instalar Ollama (ollama.com) con un modelo,
por ejemplo `llama3.2`. Si está abierto, la IA lo detecta sola.

## Qué hace
- Responde exactamente lo preguntado, con un ejemplo cuando ayuda.
- Recuerda la conversación (puedes preguntar "¿y dónde ocurre?").
- Las fotos y videos se buscan con lo que la IA entendió de tu pregunta.
- Lee la respuesta en voz alta (desmarca la casilla para silenciarla).
- Si la IA falla (sin internet, clave mala), lo dice claro en vez de inventar.

## Archivos
- `main.py`: la ventana (instala librerías y abre).
- `ia_generativa.py`: el motor.
- `clave.txt`: tu clave (se crea sola).
- `salida/`: audios generados.