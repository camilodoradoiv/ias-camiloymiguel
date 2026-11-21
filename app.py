import http.server
import socketserver
import webbrowser
import threading
import socket

# ==============================================================================
# INTELIGENCIA ARTIFICIAL DISTRIBUTIVA DE MACHINE LEARNING
# Proyecto Unificado en Python — Apertura Automática en Navegador (Sin pip)
# ==============================================================================

HTML_APLICACION = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>IA Distributiva de Machine Learning — Arquitecto de Macroprocesos</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', sans-serif;
      background-color: #0B1120;
      color: #F8FAFC;
      overflow-x: hidden;
    }
    .font-mono-code {
      font-family: 'JetBrains Mono', monospace;
    }
    @keyframes pulseRing {
      0% { transform: scale(0.95); opacity: 0.7; }
      50% { transform: scale(1.06); opacity: 0.25; }
      100% { transform: scale(0.95); opacity: 0.7; }
    }
    .pulse-ring {
      animation: pulseRing 3s infinite ease-in-out;
      transform-origin: center;
    }
    @keyframes spinSlow {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    .orbit-spin {
      animation: spinSlow 45s linear infinite;
      transform-origin: 400px 340px;
    }
    .orbit-spin-reverse {
      animation: spinSlow 60s linear infinite reverse;
      transform-origin: 400px 340px;
    }
    .node-circle {
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
    }
    .node-circle:hover {
      filter: brightness(1.2);
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0F172A;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col bg-[#0B1120] text-slate-100 select-none">

  <!-- BARRA SUPERIOR -->
  <header class="bg-[#111827]/95 border-b border-slate-800 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-30 backdrop-blur-md">
    <div class="flex items-center gap-3.5">
      <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center text-2xl shadow-lg shadow-sky-500/20">
        🧠
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-base md:text-lg font-extrabold tracking-tight text-white">
            INTELIGENCIA ARTIFICIAL DISTRIBUTIVA DE MACHINE LEARNING
          </h1>
          <span class="hidden sm:inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
            Ejecución Directa • Sin Congestión
          </span>
        </div>
        <p class="text-xs text-slate-400">
          Descomposición de Macroprocesos Complejos en Subprocesos Especializados • Arquitectura de Circunferencias y Voz IA
        </p>
      </div>
    </div>

    <!-- CONTROLES DE DOMINIO Y VOZ -->
    <div class="flex flex-wrap items-center gap-2.5">
      <button id="btn-aeropuerto" onclick="cargarMacroproceso('aeropuerto', true)"
        class="domain-btn px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-all bg-sky-500 text-slate-950 shadow-md shadow-sky-500/20">
        <span>✈️</span> Aeropuerto
      </button>
      <button id="btn-constructora" onclick="cargarMacroproceso('constructora', true)"
        class="domain-btn px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-all bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700">
        <span>🏗️</span> Casa Constructora
      </button>
      <button id="btn-policia" onclick="cargarMacroproceso('policia', true)"
        class="domain-btn px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-all bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700">
        <span>🚓</span> Policía y Seguridad
      </button>

      <div class="h-6 w-px bg-slate-700 mx-1 hidden sm:block"></div>

      <button id="btn-voz" onclick="alternarVoz()"
        class="px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-md shadow-indigo-600/25">
        <span id="icono-voz">🔊</span>
        <span id="texto-voz">Voz IA: ON</span>
      </button>
    </div>
  </header>

  <!-- CONTENIDO PRINCIPAL (3 COLUMNAS AMPLIAS) -->
  <main class="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 p-4 max-w-[1920px] w-full mx-auto">

    <!-- COLUMNA IZQUIERDA: MACROPROCESO Y ARQUITECTURA (3 cols) -->
    <section class="lg:col-span-3 bg-[#111827] border border-slate-800/90 rounded-2xl p-4 flex flex-col justify-between shadow-xl">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">📌 Macroproceso Activo</span>
          <span id="badge-nodos" class="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-sky-400">8 Subprocesos ML</span>
        </div>

        <h2 id="macro-titulo" class="text-base font-extrabold text-sky-400 leading-snug mb-2">
          1. Gestión Integral de Aeropuerto Internacional
        </h2>

        <p id="macro-resumen" class="text-xs text-slate-300 leading-relaxed mb-4 bg-slate-900/80 p-3 rounded-xl border border-slate-800">
        </p>

        <div class="border-t border-slate-800 my-3"></div>

        <h3 class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2.5">
          ⚙️ Flujo de IA Distributiva
        </h3>

        <div class="space-y-2">
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-xl p-2.5">
            <div class="text-xs font-bold text-slate-100">1. Identificación Macro</div>
            <div class="text-[11px] text-slate-400 mt-0.5">Se detecta un problema masivo que saturaría un modelo único.</div>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-xl p-2.5">
            <div class="text-xs font-bold text-slate-100">2. Planeación y Orden</div>
            <div class="text-[11px] text-slate-400 mt-0.5">Se segmenta en 8 subprocesos independientes y paralelos.</div>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-xl p-2.5">
            <div class="text-xs font-bold text-slate-100">3. Nodos ML Especializados</div>
            <div class="text-[11px] text-slate-400 mt-0.5">Cada circunferencia procesa sensores, visión, texto o voz.</div>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-xl p-2.5">
            <div class="text-xs font-bold text-slate-100">4. Orquestación Central</div>
            <div class="text-[11px] text-slate-400 mt-0.5">Los resultados se integran sin congestión en tiempo real.</div>
          </div>
        </div>
      </div>

      <button id="btn-narrar-macro" onclick="narrarMacroprocesoActual()"
        class="mt-4 w-full py-2.5 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-lg">
        <span>🎙️</span> Escuchar Explicación Completa
      </button>
    </section>

    <!-- COLUMNA CENTRAL: TOPOLOGÍA INTERACTIVA DE CIRCUNFERENCIAS (6 cols) -->
    <section class="lg:col-span-6 bg-[#111827] border border-slate-800/90 rounded-2xl p-4 flex flex-col shadow-xl">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
          <span class="text-xs font-bold uppercase tracking-wide text-slate-200">
            Topología de Circunferencias Distribuidas
          </span>
        </div>
        <span class="text-[11px] text-slate-400">
          Haz clic en cualquier circunferencia para inspeccionar y escuchar
        </span>
      </div>

      <div class="flex-1 bg-[#070B14] rounded-xl border border-slate-800/90 relative flex items-center justify-center overflow-hidden min-h-[460px]">
        <svg id="svg-topologia" viewBox="0 0 800 680" class="w-full h-full max-h-[640px]">
          <defs>
            <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.14" />
              <stop offset="70%" stop-color="#0B1120" stop-opacity="0.02" />
              <stop offset="100%" stop-color="#070B14" stop-opacity="0" />
            </radialGradient>
          </defs>
          <circle cx="400" cy="340" r="310" fill="url(#bgGlow)" />
          <g id="layer-orbitas"></g>
          <g id="layer-enlaces"></g>
          <g id="layer-nodos"></g>
          <g id="layer-centro"></g>
        </svg>

        <div class="absolute bottom-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
          <div class="bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-lg text-[11px] text-slate-300 backdrop-blur">
            <span class="font-bold text-emerald-400">● Carga Balanceada:</span> 12.5% CPU por nodo ML
          </div>
          <div class="bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-lg text-[11px] text-slate-300 backdrop-blur">
            <span class="font-bold text-sky-400">● Latencia Orquestación:</span> 14 ms
          </div>
        </div>
      </div>
    </section>

    <!-- COLUMNA DERECHA: INSPECTOR Y ETIQUETA MULTIMODAL (3 cols) -->
    <section class="lg:col-span-3 bg-[#111827] border border-slate-800/90 rounded-2xl p-4 flex flex-col justify-between shadow-xl">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">🔍 Inspector de Subproceso</span>
          <span id="inspector-id" class="font-mono-code text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">NODO #01</span>
        </div>

        <div class="bg-[#0B1120] border border-slate-800 rounded-xl p-3.5 mb-3">
          <div class="flex items-center gap-2.5 mb-2">
            <span id="sub-icono" class="text-2xl">📡</span>
            <h3 id="sub-nombre" class="text-sm font-extrabold text-white leading-tight">
              Aproximación Aérea
            </h3>
          </div>

          <div id="sub-metrica" class="text-xs font-bold text-sky-400 mb-2 bg-slate-900/90 px-2.5 py-1.5 rounded-lg border border-slate-800">
            📊 Estado: 42 vuelos en espacio aéreo
          </div>

          <p id="sub-detalle" class="text-xs text-slate-300 leading-relaxed mb-3">
            Monitoreo en tiempo real de aeronaves listas para iniciar descenso.
          </p>

          <div class="bg-indigo-950/50 border border-indigo-500/30 rounded-lg p-2.5">
            <div class="text-[10px] font-bold uppercase tracking-wider text-indigo-300 mb-0.5">🤖 Modelo Machine Learning</div>
            <div id="sub-algoritmo" class="text-xs font-semibold text-indigo-100">
              Redes Neuronales Recurrentes (LSTM) + Radar 3D
            </div>
          </div>
        </div>

        <div class="border-t border-slate-800 my-3"></div>

        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">🏷️ Etiqueta Multimodal Integrada</span>
          <span class="text-[10px] text-emerald-400 font-semibold">5 Canales Activos</span>
        </div>

        <div class="space-y-1.5">
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-lg px-3 py-1.5 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-200">📝 Texto</span>
            <span class="text-[11px] text-slate-400">Logs, reportes y registros</span>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-lg px-3 py-1.5 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-200">🖼️ Imágenes</span>
            <span class="text-[11px] text-slate-400">Planos, cámaras y escáner</span>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-lg px-3 py-1.5 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-200">🗣️ Voz</span>
            <span class="text-[11px] text-slate-400">Comandos y asistente IA</span>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-lg px-3 py-1.5 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-200">🎵 Audio</span>
            <span class="text-[11px] text-slate-400">Alertas acústicas y radio</span>
          </div>
          <div class="bg-[#0B1120] border border-slate-800/80 rounded-lg px-3 py-1.5 flex items-center justify-between">
            <span class="text-xs font-bold text-slate-200">🎬 Video</span>
            <span class="text-[11px] text-slate-400">Monitoreo en tiempo real</span>
          </div>
        </div>
      </div>

      <!-- SUBTÍTULOS DEL ASISTENTE DE VOZ -->
      <div class="mt-3 pt-3 border-t border-slate-800">
        <div class="flex items-center justify-between mb-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">💬 Asistente de Voz IA (En Vivo)</span>
          <span id="voz-estado-badge" class="text-[10px] text-emerald-400 font-semibold">● Listo</span>
        </div>
        <div id="voz-subtitulo" class="bg-[#0B1120] border border-emerald-500/30 rounded-xl p-2.5 text-xs italic text-emerald-300 leading-relaxed min-h-[54px]">
          🎙️ «Selecciona cualquier sector o circunferencia para escuchar la explicación detallada de la IA.»
        </div>
      </div>
    </section>
  </main>

  <script>
    const DATOS_MACROPROCESOS = {
      aeropuerto: {
        titulo: "1. Gestión Integral de Aeropuerto Internacional",
        colorTema: "#38BDF8",
        colorSecundario: "#0284C7",
        btnClass: "bg-sky-500 text-slate-950 shadow-md shadow-sky-500/20",
        narrarBtnClass: "bg-sky-600 hover:bg-sky-500",
        icono: "✈️",
        resumen:
          "Un aeropuerto internacional es un macroproceso masivo. Si un único modelo de Machine Learning intentara gestionar vuelos, pistas, combustible y pasajeros a la vez, colapsaría por congestión. La IA Distributiva divide esta carga en 8 nodos especializados.",
        narracionGeneral:
          "Bienvenido al macroproceso de gestión de un aeropuerto internacional. Para evitar la congestión del sistema central, dividimos la operación en ocho subprocesos distribuidos de Machine Learning: aproximación aérea, asignación de pistas, despegues, mantenimiento preventivo, carga de combustible, inspección de neumáticos, conexiones de rutas y flujo de pasajeros.",
        subprocesos: [
          {
            id: "aprox",
            nombre: "Aproximación Aérea",
            icono: "📡",
            metrica: "42 vuelos en espacio aéreo",
            detalle: "Monitoreo en tiempo real de aeronaves listas para iniciar descenso controlado.",
            algoritmo: "Redes Neuronales Recurrentes (LSTM) + Radar 3D",
            narracion: "Subproceso de aproximación aérea. Analizando cuarenta y dos aeronaves listas para aterrizar mediante redes neuronales recurrentes."
          },
          {
            id: "pistas_arr",
            nombre: "Pistas Aterrizaje",
            icono: "🛬",
            metrica: "Pistas 01L y 01R activas",
            detalle: "Cálculo óptimo de pista según viento cruzado, peso de aeronave y ocupación.",
            algoritmo: "Aprendizaje por Refuerzo (Q-Learning)",
            narracion: "Subproceso de asignación de pistas de aterrizaje. Optimizando el uso de pistas según condiciones meteorológicas."
          },
          {
            id: "despegues",
            nombre: "Secuencia Despegues",
            icono: "🛫",
            metrica: "Intervalo: 90 segundos",
            detalle: "Ordenamiento de salidas y asignación de pista de despegue sin turbulencia de estela.",
            algoritmo: "Optimización Combinatoria + IA Multi-Agente",
            narracion: "Subproceso de despegues. Coordinando salidas cada noventa segundos para maximizar la capacidad de pista."
          },
          {
            id: "mantenimiento",
            nombre: "Mantenimiento",
            icono: "🔧",
            metrica: "99.4% disponibilidad flota",
            detalle: "Detección temprana de fallas en turbinas y sistemas hidráulicos al llegar a puerta.",
            algoritmo: "Random Forest + Sensores IoT de Telemetría",
            narracion: "Subproceso de mantenimiento predictivo. Evaluando sensores de telemetría para detectar desgaste antes de que ocurra una falla."
          },
          {
            id: "combustible",
            nombre: "Combustible",
            icono: "⛽",
            metrica: "18 camiones cisterna activos",
            detalle: "Cálculo exacto de litraje por ruta, clima y logística de abastecimiento.",
            algoritmo: "Regresión Gradiente (XGBoost)",
            narracion: "Subproceso de suministro de combustible. Calculando el volumen exacto requerido según distancia y vientos en ruta."
          },
          {
            id: "llantas",
            nombre: "Revisión Llantas",
            icono: "🛞",
            metrica: "Visión artificial en rodaje",
            detalle: "Escaneo láser y visión por computadora para desgaste y presión de neumáticos.",
            algoritmo: "Redes Convolucionales (CNN - YOLOv8)",
            narracion: "Subproceso de inspección de neumáticos. Usando visión artificial para verificar presión y desgaste en cada aterrizaje."
          },
          {
            id: "conexiones",
            nombre: "Conexiones y Rutas",
            icono: "🌐",
            metrica: "124 destinos sincronizados",
            detalle: "Gestión dinámica de puertas de embarque, orígenes, destinos y escalas.",
            algoritmo: "Graph Neural Networks (GNN)",
            narracion: "Subproceso de conexiones internacionales. Sincronizando orígenes, escalas y destinos mediante redes de grafos."
          },
          {
            id: "pasajeros",
            nombre: "Flujo Pasajeros",
            icono: "🧳",
            metrica: "14,850 viajeros/hora",
            detalle: "Predicción de filas en migración, seguridad y distribución de equipaje.",
            algoritmo: "Series Temporales + Visión Computacional",
            narracion: "Subproceso de flujo de pasajeros. Prediciendo demanda en filtros de seguridad y bandas de equipaje."
          }
        ]
      },
      constructora: {
        titulo: "2. Casa Constructora y Megaproyectos Urbanos",
        colorTema: "#F59E0B",
        colorSecundario: "#D97706",
        btnClass: "bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20",
        narrarBtnClass: "bg-amber-600 hover:bg-amber-500",
        icono: "🏗️",
        resumen:
          "Una empresa constructora gestiona simultáneamente diseño arquitectónico, cimentación, cadena de suministro, maquinaria pesada y seguridad industrial. La IA Distributiva evita cuellos de botella asignando un nodo inteligente a cada frente de obra.",
        narracionGeneral:
          "Bienvenido al macroproceso de casa constructora e ingeniería civil. Dividimos la ejecución de obras en ocho subprocesos especializados de Machine Learning: geotecnia y suelos, diseño estructural BIM, logística de materiales, control de maquinaria, seguridad laboral, presupuestos y costos, ruta crítica y control de calidad.",
        subprocesos: [
          {
            id: "suelos",
            nombre: "Geotecnia y Suelos",
            icono: "⛰️",
            metrica: "Capacidad portante: 3.8 kg/cm²",
            detalle: "Análisis de estratos, humedad y resistencia sísmica del terreno antes de cimentar.",
            algoritmo: "Máquinas de Soporte Vectorial (SVM)",
            narracion: "Subproceso de geotecnia y suelos. Evaluando resistencia sísmica y composición del terreno antes de excavar."
          },
          {
            id: "bim",
            nombre: "Diseño BIM 3D",
            icono: "📐",
            metrica: "0 colisiones detectadas",
            detalle: "Optimización de vigas, columnas y redes hidráulicas en modelos tridimensionales.",
            algoritmo: "Diseño Generativo + Deep Learning",
            narracion: "Subproceso de diseño estructural B I M. Detectando interferencias entre estructuras y redes eléctricas en tres dimensiones."
          },
          {
            id: "materiales",
            nombre: "Materiales Obra",
            icono: "🧱",
            metrica: "Cemento y acero Just-In-Time",
            detalle: "Predicción de consumo de hormigón, varilla y acabados sin sobreinventario.",
            algoritmo: "Modelos ARIMA + Optimización Lineal",
            narracion: "Subproceso de logística de materiales. Coordinando entregas de concreto premezclado y acero justo a tiempo."
          },
          {
            id: "maquinaria",
            nombre: "Grúas y Maquinaria",
            icono: "🚜",
            metrica: "14 excavadoras y 3 grúas",
            detalle: "Asignación óptima de maquinaria pesada y mantenimiento preventivo en campo.",
            algoritmo: "Aprendizaje por Refuerzo Multi-Agente",
            narracion: "Subproceso de control de maquinaria pesada. Optimizando ciclos de carga de grúas torre y excavadoras."
          },
          {
            id: "seguridad",
            nombre: "Seguridad SST",
            icono: "🦺",
            metrica: "100% uso de casco y arnés",
            detalle: "Cámaras con IA que alertan ingreso a zonas de riesgo o falta de elementos de protección.",
            algoritmo: "Visión Artificial en Tiempo Real (CNN)",
            narracion: "Subproceso de seguridad industrial. Verificando el uso de cascos, arneses y perímetros seguros en toda la obra."
          },
          {
            id: "costos",
            nombre: "Presupuesto",
            icono: "💰",
            metrica: "Desviación: -0.8% (Óptimo)",
            detalle: "Detección de sobrecostos en tiempo real y fluctuación de precios de insumos.",
            algoritmo: "Gradient Boosting + Análisis Predictivo",
            narracion: "Subproceso de control presupuestal. Monitoreando costos unitarios y evitando desviaciones financieras."
          },
          {
            id: "cronograma",
            nombre: "Ruta Crítica CPM",
            icono: "📅",
            metrica: "Avance de obra: 68.5%",
            detalle: "Reprogramación automática ante lluvias o retrasos en cadena de suministro.",
            algoritmo: "Redes Bayesianas + Simulación Monte Carlo",
            narracion: "Subproceso de ruta crítica. Ajustando el cronograma de obra dinámicamente ante cambios climáticos."
          },
          {
            id: "calidad",
            nombre: "Calidad Concreto",
            icono: "🏢",
            metrica: "Resistencia f'c = 280 kg/cm²",
            detalle: "Predicción de fraguado y resistencia estructural mediante sensores térmicos.",
            algoritmo: "Redes Neuronales Profundas (MLP)",
            narracion: "Subproceso de control de calidad. Verificando la resistencia del concreto y acabados arquitectónicos."
          }
        ]
      },
      policia: {
        titulo: "3. Seguridad Ciudadana y Operaciones de Policía",
        colorTema: "#10B981",
        colorSecundario: "#059669",
        btnClass: "bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20",
        narrarBtnClass: "bg-emerald-600 hover:bg-emerald-500",
        icono: "🚓",
        resumen:
          "La seguridad pública de una metrópoli exige coordinar llamadas de emergencia, patrullaje, cámaras urbanas, análisis criminalístico y respuesta táctica. La IA Distributiva procesa cada frente en milisegundos sin saturar el centro de mando.",
        narracionGeneral:
          "Bienvenido al macroproceso de seguridad ciudadana y operaciones de policía. Para garantizar una respuesta rápida y precisa, dividimos la operación en ocho subprocesos de Machine Learning: despacho de emergencias, patrullaje predictivo, videovigilancia inteligente, análisis forense, control vial, ciberseguridad, logística de unidades y frentes de seguridad.",
        subprocesos: [
          {
            id: "emergencias",
            nombre: "Línea 123 / 911",
            icono: "📞",
            metrica: "Respuesta: 3 min 40 s",
            detalle: "Clasificación automática de prioridad y geolocalización de llamadas críticas.",
            algoritmo: "Procesamiento de Lenguaje Natural (NLP)",
            narracion: "Subproceso de despacho de emergencias. Clasificando llamadas por nivel de urgencia mediante procesamiento de lenguaje natural."
          },
          {
            id: "patrullaje",
            nombre: "Patrullaje",
            icono: "🚔",
            metrica: "85 cuadrantes monitoreados",
            detalle: "Identificación de zonas y horarios con mayor probabilidad de incidentes.",
            algoritmo: "Mapas de Calor Espacio-Temporales",
            narracion: "Subproceso de patrullaje predictivo. Distribuyendo cuadrantes preventivos según patrones históricos y horarios."
          },
          {
            id: "camaras",
            nombre: "Cámaras LPR",
            icono: "📹",
            metrica: "2,400 cámaras conectadas",
            detalle: "Lectura automática de placas de vehículos reportados y detección de anomalías.",
            algoritmo: "Visión por Computadora + OCR Profundo",
            narracion: "Subproceso de videovigilancia inteligente. Analizando lecturas de placas y alertas perimetrales en tiempo real."
          },
          {
            id: "forense",
            nombre: "Análisis Forense",
            icono: "🔍",
            metrica: "Correlación de patrones",
            detalle: "Vinculación de evidencia digital, balística y modus operandi entre casos.",
            algoritmo: "Clustering Jerárquico + Grafos de Vínculos",
            narracion: "Subproceso de análisis criminalístico. Conectando evidencias y patrones para apoyar investigaciones judiciales."
          },
          {
            id: "transito",
            nombre: "Control Vial",
            icono: "🚦",
            metrica: "Corredores verdes activos",
            detalle: "Sincronización de semáforos para paso rápido de patrullas y ambulancias.",
            algoritmo: "Aprendizaje por Refuerzo en Redes Viales",
            narracion: "Subproceso de control vial. Abriendo corredores semafóricos para unidades de emergencia."
          },
          {
            id: "ciber",
            nombre: "Ciberpatrullaje",
            icono: "🛡️",
            metrica: "Detección amenazas red",
            detalle: "Monitoreo de ataques informáticos, suplantación y delitos financieros.",
            algoritmo: "Autoencoders de Detección de Anomalías",
            narracion: "Subproceso de ciberseguridad policial. Detectando fraudes digitales y protegiendo infraestructuras críticas."
          },
          {
            id: "flota_pol",
            nombre: "Flota y Unidades",
            icono: "🚁",
            metrica: "120 patrullas + 2 helicópteros",
            detalle: "Asignación de unidad más cercana según tráfico y nivel de equipamiento.",
            algoritmo: "Algoritmo A* + Predicción de Tráfico",
            narracion: "Subproceso de logística de unidades. Calculando la ruta más rápida para la patrulla o helicóptero más cercano."
          },
          {
            id: "comunidad",
            nombre: "Red Vecinal",
            icono: "🤝",
            metrica: "310 frentes activos",
            detalle: "Integración de alertas comunitarias verificadas con estaciones locales.",
            algoritmo: "Clasificación Bayesiana de Reportes",
            narracion: "Subproceso de frentes de seguridad ciudadana. Conectando reportes vecinales verificados con los cuadrantes locales."
          }
        ]
      }
    };

    let macroprocesoActual = "aeropuerto";
    let subprocesoSeleccionadoId = "aprox";
    let vozActiva = true;

    function hablar(texto) {
      const subtituloEl = document.getElementById("voz-subtitulo");
      const badgeEl = document.getElementById("voz-estado-badge");
      subtituloEl.textContent = `🎙️ «${texto}»`;

      if (!vozActiva || !("speechSynthesis" in window)) {
        return;
      }

      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(texto);
      utterance.lang = "es-ES";
      utterance.rate = 1.04;
      utterance.pitch = 1.0;

      const voces = window.speechSynthesis.getVoices();
      const vozEs = voces.find(v => v.lang.startsWith("es"));
      if (vozEs) utterance.voice = vozEs;

      utterance.onstart = () => {
        badgeEl.textContent = "● Hablando...";
        badgeEl.className = "text-[10px] text-amber-400 font-bold animate-pulse";
      };
      utterance.onend = () => {
        badgeEl.textContent = "● Listo";
        badgeEl.className = "text-[10px] text-emerald-400 font-semibold";
      };

      window.speechSynthesis.speak(utterance);
    }

    function alternarVoz() {
      vozActiva = !vozActiva;
      const btn = document.getElementById("btn-voz");
      const icono = document.getElementById("icono-voz");
      const texto = document.getElementById("texto-voz");

      if (vozActiva) {
        btn.className = "px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-md shadow-indigo-600/25";
        icono.textContent = "🔊";
        texto.textContent = "Voz IA: ON";
        hablar("Asistente de voz activado.");
      } else {
        window.speechSynthesis.cancel();
        btn.className = "px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-1.5 bg-slate-700 text-slate-300 transition-all";
        icono.textContent = "🔇";
        texto.textContent = "Voz IA: OFF";
        document.getElementById("voz-subtitulo").textContent = "🔇 Voz silenciada. Activa 'Voz IA' para escuchar.";
      }
    }

    function cargarMacroproceso(clave, reproducirVoz = true) {
      macroprocesoActual = clave;
      const datos = DATOS_MACROPROCESOS[clave];

      ["aeropuerto", "constructora", "policia"].forEach(dom => {
        const b = document.getElementById(`btn-${dom}`);
        if (dom === clave) {
          b.className = `domain-btn px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-all ${datos.btnClass}`;
        } else {
          b.className = "domain-btn px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-all bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700";
        }
      });

      const tituloEl = document.getElementById("macro-titulo");
      tituloEl.textContent = datos.titulo;
      tituloEl.style.color = datos.colorTema;

      document.getElementById("macro-resumen").textContent = datos.resumen;

      const btnNarrar = document.getElementById("btn-narrar-macro");
      btnNarrar.className = `mt-4 w-full py-2.5 px-4 rounded-xl ${datos.narrarBtnClass} text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-lg`;

      subprocesoSeleccionadoId = datos.subprocesos[0].id;
      seleccionarSubproceso(datos.subprocesos[0], 0, false);

      if (reproducirVoz) {
        hablar(datos.narracionGeneral);
      }
    }

    function narrarMacroprocesoActual() {
      const datos = DATOS_MACROPROCESOS[macroprocesoActual];
      hablar(datos.narracionGeneral);
    }

    function seleccionarSubproceso(sub, index, reproducirVoz = true) {
      subprocesoSeleccionadoId = sub.id;
      const datos = DATOS_MACROPROCESOS[macroprocesoActual];

      document.getElementById("inspector-id").textContent = `NODO #0${index + 1}`;
      document.getElementById("sub-icono").textContent = sub.icono;
      document.getElementById("sub-nombre").textContent = sub.nombre;

      const metricaEl = document.getElementById("sub-metrica");
      metricaEl.textContent = `📊 Estado: ${sub.metrica}`;
      metricaEl.style.color = datos.colorTema;

      document.getElementById("sub-detalle").textContent = sub.detalle;
      document.getElementById("sub-algoritmo").textContent = sub.algoritmo;

      dibujarTopologia();

      if (reproducirVoz) {
        hablar(sub.narracion);
      }
    }

    function dibujarTopologia() {
      const datos = DATOS_MACROPROCESOS[macroprocesoActual];
      const colorTema = datos.colorTema;
      const colorSec = datos.colorSecundario;
      const subprocesos = datos.subprocesos;

      const cx = 400;
      const cy = 340;
      const radioOrbita = 228;
      const radioCentral = 84;
      const radioNodo = 52;

      const layerOrbitas = document.getElementById("layer-orbitas");
      const layerEnlaces = document.getElementById("layer-enlaces");
      const layerNodos = document.getElementById("layer-nodos");
      const layerCentro = document.getElementById("layer-centro");

      layerOrbitas.innerHTML = `
        <circle cx="${cx}" cy="${cy}" r="${radioOrbita * 1.28}" fill="none" stroke="#1E293B" stroke-width="1.5" stroke-dasharray="6 8" class="orbit-spin" />
        <circle cx="${cx}" cy="${cy}" r="${radioOrbita}" fill="none" stroke="#334155" stroke-width="2" stroke-dasharray="10 6" class="orbit-spin-reverse" />
        <circle cx="${cx}" cy="${cy}" r="${radioOrbita * 0.65}" fill="none" stroke="#1E293B" stroke-width="1.5" stroke-dasharray="3 6" />
      `;

      let enlacesHTML = "";
      let nodosHTML = "";

      subprocesos.forEach((sub, i) => {
        const angulo = (2 * Math.PI * i / subprocesos.length) - (Math.PI / 2);
        const nx = cx + radioOrbita * Math.cos(angulo);
        const ny = cy + radioOrbita * Math.sin(angulo);
        const esActivo = sub.id === subprocesoSeleccionadoId;

        enlacesHTML += `
          <line x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}"
            stroke="${esActivo ? colorTema : '#334155'}"
            stroke-width="${esActivo ? 3.5 : 1.8}"
            stroke-opacity="${esActivo ? 1 : 0.7}" />
        `;

        if (esActivo) {
          const mx = (cx + nx) / 2;
          const my = (cy + ny) / 2;
          enlacesHTML += `
            <circle cx="${mx}" cy="${my}" r="5" fill="${colorTema}" class="pulse-ring" />
          `;
        }

        const halo = esActivo
          ? `<circle cx="${nx}" cy="${ny}" r="${radioNodo + 9}" fill="none" stroke="${colorTema}" stroke-width="2.5" class="pulse-ring" />`
          : "";

        nodosHTML += `
          <g class="node-circle" onclick="seleccionarSubproceso(DATOS_MACROPROCESOS['${macroprocesoActual}'].subprocesos[${i}], ${i}, true)">
            ${halo}
            <circle cx="${nx}" cy="${ny}" r="${radioNodo}"
              fill="${esActivo ? colorSec : '#111827'}"
              stroke="${esActivo ? colorTema : '#475569'}"
              stroke-width="${esActivo ? 3 : 2}" />
            <text x="${nx}" y="${ny - 10}" text-anchor="middle" font-size="22" fill="#FFFFFF">${sub.icono}</text>
            <text x="${nx}" y="${ny + 14}" text-anchor="middle" font-size="11" font-weight="700" fill="#F8FAFC">${sub.nombre}</text>
            <text x="${nx}" y="${ny + 28}" text-anchor="middle" font-size="9" font-weight="600" fill="${esActivo ? '#FFFFFF' : '#94A3B8'}">Nodo 0${i + 1}</text>
          </g>
        `;
      });

      layerEnlaces.innerHTML = enlacesHTML;
      layerNodos.innerHTML = nodosHTML;

      layerCentro.innerHTML = `
        <g onclick="narrarMacroprocesoActual()" class="node-circle">
          <circle cx="${cx}" cy="${cy}" r="${radioCentral + 10}" fill="none" stroke="${colorTema}" stroke-width="1.5" stroke-dasharray="6 4" class="orbit-spin" />
          <circle cx="${cx}" cy="${cy}" r="${radioCentral}" fill="#090D16" stroke="${colorTema}" stroke-width="4" />
          <text x="${cx}" y="${cy - 18}" text-anchor="middle" font-size="28" fill="#FFFFFF">${datos.icono}</text>
          <text x="${cx}" y="${cy + 10}" text-anchor="middle" font-size="12" font-weight="800" fill="${colorTema}">MACROPROCESO</text>
          <text x="${cx}" y="${cy + 25}" text-anchor="middle" font-size="11" font-weight="700" fill="#F8FAFC">IA DISTRIBUTIVA</text>
          <text x="${cx}" y="${cy + 41}" text-anchor="middle" font-size="9" fill="#94A3B8">8 Nodos ML Activos</text>
        </g>
      `;
    }

    if ("speechSynthesis" in window) {
      window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
    }
    window.addEventListener("DOMContentLoaded", () => {
      cargarMacroproceso("aeropuerto", false);
    });
  </script>
</body>
</html>
"""


class ManejadorApp(http.server.BaseHTTPRequestHandler):
    """Servidor HTTP ligero que entrega la aplicación web interactiva directamente."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_APLICACION.encode("utf-8"))

    def log_message(self, format, *args):
        # Silenciar registros innecesarios en consola
        pass


def obtener_puerto_libre():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def iniciar_aplicacion():
    puerto = obtener_puerto_libre()
    url = f"http://127.0.0.1:{puerto}"

    servidor = socketserver.TCPServer(("127.0.0.1", puerto), ManejadorApp)
    hilo_servidor = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo_servidor.start()

    print("=" * 72)
    print("🧠 IA DISTRIBUTIVA DE MACHINE LEARNING — ARQUITECTO DE MACROPROCESOS")
    print("=" * 72)
    print(f"✅ Abriendo automáticamente en tu navegador: {url}")
    print("ℹ️  No requiere instalar librerías ni ejecutar comandos en terminal.")
    print("🛑 Presiona Ctrl+C o detén la ejecución en Visual Studio para cerrar.")
    print("=" * 72)

    # Abrir automáticamente el navegador predeterminado en la página
    webbrowser.open(url)

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print()
        print("Cerrando servidor local...")
        servidor.shutdown()
        servidor.server_close()


if __name__ == "__main__":
    iniciar_aplicacion()