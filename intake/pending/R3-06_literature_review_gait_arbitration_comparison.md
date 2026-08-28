# R3-06 — Revisión de literatura: clasificación horizontal y tabla comparativa (Basal Ganglia vs. CPG vs. RL) — PENDIENTE

**Owner asignado: Cejas — única tarea de mañana, dedicación completa del día. Prioriza calidad y rigor sobre
velocidad; esto no es un "quick pass".**

**Por qué se reabre:** `PROGRESS.md` marcaba `R3-06` como `pending` con la nota "narrative comparison already
exists, likely just needs converting to a table" — un intento anterior lo dio por resuelto de forma insuficiente
(el revisor no quedó satisfecho). Este documento reemplaza ese diagnóstico superficial con un plan completo,
verificado contra el texto actual línea por línea, no una suposición.

## 0. Comentario textual del revisor (R3, verbatim — ancla de todo lo que sigue)

> "The literature review fails to systematically summarize existing bio-inspired gait arbitration research. It
> lacks horizontal classification and comparative tables of basal ganglia, CPG, and RL-based action selection
> algorithms, so the manuscript cannot clearly highlight its unique technical innovations against existing
> bio-locomotion controllers."

Cuatro exigencias explícitas, ninguna opcional:
1. **Resumen sistemático** de la investigación existente en arbitraje de marcha bio-inspirado (no solo
   mencionar trabajos sueltos en prosa).
2. **Clasificación horizontal** — organizar los trabajos por dimensiones comparables, no por orden cronológico
   de aparición en el texto.
3. **Tabla(s) comparativa(s)** de específicamente **tres paradigmas**: Basal Ganglia, CPG, y selección de acción
   basada en RL.
4. El resultado debe **resaltar claramente las innovaciones técnicas únicas** del paper frente a controladores
   bio-locomotores existentes — no es un ejercicio bibliográfico neutral, tiene que dejar claro **por qué
   importa lo que este paper aporta**.

## 1. Escaneo del estado actual (`sections/introduction.tex`, líneas 7-11 — texto completo, no resumido)

**Párrafo de plataformas híbridas (línea 7):** cubre bien la familia ANYmal-on-wheels (Bjelonic2019KeepRollin,
bjelonic2019, Bjelonic2022OfflineMotion, Lee2024Science), CENTAURO (Kashiri2019CENTAURO, Klamt2019CENTAURO),
Ascento (Klemm2019Ascento), y trabajos recientes (Liu2024Max, Cui2025FLORES, Jiang2025RTaichi) — esto es
contexto de plataformas, **no de mecanismos de arbitraje**, así que no cuenta para lo que pide el revisor
directamente, pero sí es la evidencia de que "el campo converge en locomoción híbrida" — mantener como está.

**Párrafo de mecanismos de switching (línea 9):** el único lugar que hoy compara mecanismos de decisión, y lo
hace en una sola oración: *"locomotion mode switching is resolved either heuristically through hand-coded
threshold logic \citep{Bjelonic2019KeepRollin,Kashiri2019CENTAURO}, by model predictive control
\citep{bjelonic2019,Bjelonic2022OfflineMotion}, or by end-to-end RL policies that encode switching implicitly as
a black-box behavior \citep{Lee2024Science,Humphreys2025BioInspired}."* Después afirma que ninguno usa
arbitraje neurobiológicamente interpretable y presenta basal ganglia como la alternativa.

**Veredicto honesto de por qué esto no satisface al revisor, aunque menciona los tres paradigmas:**
- **No es una tabla ni una clasificación horizontal** — es una oración con 5 citas encadenadas. El revisor pide
  explícitamente "comparative tables", plural.
- **CPG no aparece aquí en absoluto como mecanismo de arbitraje** — el párrafo 9 solo compara
  threshold-logic/MPC/RL. CPG aparece más adelante (línea 11) pero **exclusivamente como generador rítmico de
  la marcha** ("For the rhythmic generation of the quadrupedal walking gait, the present platform integrates
  central pattern generators (CPGs)... this combination of BG arbitration above and CPG execution below forms
  a hierarchical neural stack"). El revisor pide CPG como uno de los **tres paradigmas de selección de
  acción/arbitraje**, no como capa de ejecución subordinada — esto es una laguna real, no solo un problema de
  formato.
- **RL-para-arbitraje está débilmente representado** — Lee2024Science es RL para todo el controlador de
  locomoción (incluye planeación global, no es específicamente sobre *selección de modo/marcha*), y
  Humphreys2025BioInspired no se ha verificado si trata específicamente selección de acción vs. otra cosa
  bio-inspirada. Podría no alcanzar para sostener una columna completa de la tabla.
- **Basal ganglia sí está bien cubierto** (línea 11: Gurney2001a/b, Prescott2006Robot, Girard2003Basal,
  sarvestani2013computational, Baston2015Biologically, Prescott2024Simulated) — esta columna probablemente **no
  necesita papers nuevos**, solo reorganización en tabla.

**Conclusión del escaneo:** no es un simple "convertir prosa en tabla" — la columna CPG-como-arbitraje está
genuinamente vacía (los CPG citados hoy son para ejecución, no para selección) y la columna RL-arbitraje es
débil. Sí hace falta buscar literatura nueva antes de poder construir la tabla honestamente. Ver §2.

## 2. Análisis de vacíos — qué buscar específicamente

No es "buscar más papers de robots" en general — es buscar papers que respondan a la pregunta exacta que el
revisor plantea: **¿cómo deciden otros sistemas bio-inspirados CUÁL comportamiento/marcha ejecutar, no cómo lo
ejecutan una vez decidido?**

- **CPG como mecanismo de arbitraje/selección** (no solo generación rítmica): buscar trabajos donde
  redes CPG acopladas o moduladas por parámetros deciden la transición entre marchas/modos —
  ej. bifurcaciones/cambios de fase entre osciladores acoplados que seleccionan marcha (trote↔galope↔caminata),
  arquitecturas CPG multi-capa con una capa de "selección" explícita sobre CPGs candidatos, CPG modulado por
  señales sensoriales que actúa como interruptor de comportamiento. Diferenciar explícitamente de CPGs que solo
  generan el patrón rítmico de una única marcha ya seleccionada externamente (eso NO cuenta para esta columna).
- **RL para arbitraje/selección de modo específicamente** (no RL para todo el pipeline de locomoción): buscar
  RL aplicado a la decisión de *cuándo cambiar* de marcha/modo/comportamiento (política de alto nivel sobre un
  conjunto discreto de comportamientos/marchas), jerárquico RL con una política "gating"/"switching" sobre
  sub-políticas o controladores de bajo nivel entrenados por separado. Verificar si `Humphreys2025BioInspired`
  (ya citado) realmente encaja aquí antes de asumirlo.
- **Basal ganglia / WTA:** revisar si hace falta 1-2 papers adicionales de aplicación robótica reciente (2022+)
  más allá de los ya citados, para que la columna no se vea desactualizada frente a las otras dos si estas se
  actualizan con literatura 2023-2025.

**Criterio para decidir "necesito más papers" columna por columna:** cada una de las 3 columnas debe tener
mínimo 2-3 trabajos representativos, con al menos uno de los tres siendo relativamente reciente (2020+), para
que la tabla se vea como una revisión seria y no como relleno. **No añadir papers solo para llenar la tabla** —
si una columna genuinamente tiene poca literatura de arbitraje puro (posible para CPG, ya que la mayoría de la
literatura CPG es sobre generación, no selección), decirlo explícitamente en el texto en vez de forzar citas
tangenciales — eso en sí mismo es una observación válida que refuerza la novedad del paper.

## 3. Protocolo de búsqueda

1. Fuentes: Google Scholar, Semantic Scholar, arXiv, y buscador del sitio del editor/DOI cuando el resultado
   venga de una revista/conferencia específica. Usar las herramientas de búsqueda web disponibles en la sesión
   — si no están disponibles, **detenerse y decirlo explícitamente**, no improvisar referencias de memoria.
2. Queries sugeridas (punto de partida, no lista cerrada): "CPG gait transition selection", "central pattern
   generator mode switching robot", "coupled oscillator gait selection legged robot", "reinforcement learning
   gait switching hierarchical", "RL high-level locomotion mode selection policy", "basal ganglia robot action
   selection 2023", "winner-take-all gait arbitration robot".
3. Para cada candidato encontrado, registrar de inmediato (no después, de memoria): título exacto, autores
   completos, venue/año, DOI o URL de la fuente donde se encontró — este registro es el insumo directo del
   protocolo de verificación de §4, no un paso aparte.
4. Priorizar por relevancia real a "selección/arbitraje", no por cercanía temática general con robótica
   bio-inspirada — un paper excelente de CPG que no tiene ningún componente de selección/transición no sirve
   para esta tabla, aunque sea buena literatura de fondo.

## 4. Protocolo de verificación de existencia (obligatorio para CADA referencia nueva, sin excepción)

**Contexto del porqué esto es obligatorio y no solo buena práctica:** el equipo ya ha tenido casos de
referencias incluidas en el paper que no existen o con nombres de título/autor erróneos. Este protocolo existe
específicamente para que eso no vuelva a pasar aquí.

Para cada referencia candidata, en este orden:

1. **Encontrar la fuente primaria real** — no un resumen de segunda mano, no una mención en otro paper, no
   "recordar" el paper. La fuente es la página del editor (IEEE Xplore/ACM DL/Springer/etc.), el abstract de
   arXiv, o el registro de DOI (`doi.org/<DOI>` debe resolver a una página que coincide con el título/autores
   que se van a citar).
2. **Cruzar contra una segunda fuente independiente** — Semantic Scholar o Google Scholar, buscando por el
   título exacto. Título, lista completa de autores, venue y año deben coincidir entre ambas fuentes. Una
   discrepancia (autor faltante, año distinto, título parecido pero no idéntico) es motivo para **descartar el
   candidato o investigar más**, no para ajustar el nombre para que "encaje".
3. **Nunca escribir el BibTeX a mano desde memoria.** Exportar la cita directamente desde la fuente verificada
   (botón "Cite"/"Export BibTeX" de Google Scholar, Semantic Scholar, o del sitio del editor/DOI) — el texto del
   BibTeX debe venir de un exportador real, no ser tecleado campo por campo.
4. **Revisar duplicados:** buscar en `assets/references.bib` (50 entradas actuales) si el paper ya está citado
   bajo otra clave antes de añadirlo de nuevo.
5. **Registrar la evidencia**, no solo el resultado — para cada referencia nueva, dejar en este mismo documento
   (nueva sección "Referencias verificadas", añadir según se van confirmando) una fila con: clave BibTeX
   propuesta, título, DOI/URL de la fuente primaria, URL de la fuente de cruce (paso 2), y una nota de una línea
   de por qué encaja en la columna (CPG-arbitraje / RL-arbitraje / basal ganglia).
6. **Validación manual final, obligatoria antes de tocar `assets/references.bib` o `sections/introduction.tex`:**
   presentar la tabla completa de referencias nuevas (con su evidencia) al autor para aprobación explícita.
   **No fusionar entradas nuevas al `.bib` ni citarlas en el texto sin ese visto bueno** — este es el paso que
   existe específicamente para atrapar cualquier error que el protocolo automático no haya detectado.

## 5. Exportación e integración BibTeX

- Formato: seguir el estilo ya presente en `assets/references.bib` (claves tipo `Autor2025PalabraClave` o
  `autor2025`, ver ejemplos existentes como `Bjelonic2019KeepRollin`, `sarvestani2013computational`) — revisar
  las ~50 entradas actuales antes de inventar un estilo de clave distinto.
- Insertar las entradas nuevas ya aprobadas (paso 6 de §4) al final de `assets/references.bib`, agrupadas con un
  comentario `% R3-06 — gait arbitration comparison, added <fecha>` para que sean identificables como grupo.
- Verificar que `scripts/validate_tex.sh` no falle por una clave BibTeX duplicada o mal formada antes de seguir.

## 6. Integración a la escritura — sin contradecir lo ya existente

- **No reemplazar** el párrafo de la línea 9 (`hand-coded threshold logic`/MPC/RL) — ese sigue siendo válido
  para el contexto de plataformas híbridas específicas. La tabla nueva es un **complemento**, específicamente
  sobre arbitraje bio-inspirado, no un reemplazo de esa oración.
- **Sí reformular** la frase de la línea 11 que hoy encuadra CPG únicamente como "execution" — debe quedar claro
  que el paper conoce y considera la alternativa de usar CPG (o RL) como mecanismo de arbitraje, y por qué se
  eligió basal ganglia en su lugar (esto es exactamente lo que "resaltar las innovaciones únicas" significa en
  la práctica: no basta con mencionar los otros paradigmas, hay que decir explícitamente por qué el enfoque de
  este paper es distinto/mejor para este problema).
- Insertar la tabla comparativa (ver esqueleto en §7) inmediatamente después del párrafo de la línea 9 o al
  final del bloque de la línea 11 (decisión editorial de Cejas según qué fluya mejor — probar ambas ubicaciones
  antes de fijar una).
- Todo el texto nuevo/reescrito envuelto en `\revblue{}` (regla permanente del proyecto).

## 7. Esqueleto de la tabla comparativa (llenar con los papers verificados, no inventar contenido de columna)

```latex
\begin{table}[htbp]
\centering
\caption{\revblue{Horizontal comparison of bio-inspired action-selection paradigms for gait/mode arbitration
in legged and hybrid locomotion.}}
\label{tab:action_selection_comparison}
\begin{tabularx}{\textwidth}{l l X X}
\toprule
\textbf{Paradigm} & \textbf{Representative work(s)} & \textbf{Arbitration mechanism} & \textbf{Limitation relative to this work} \\
\midrule
Basal Ganglia (WTA) & \citep{...} & Salience-driven disinhibition, competing channels & (llenar tras revisar qué distingue a este paper de los ya citados) \\
CPG-based & \citep{...} & (llenar según lo encontrado en §2/§3 — si la literatura de arbitraje puro es escasa, decirlo aquí explícitamente en vez de forzar una fila débil) & \\
RL-based & \citep{...} & High-level policy over discrete behavior/gait set & Implicit, non-interpretable decision boundary (black-box) \\
\bottomrule
\end{tabularx}
\end{table}
```

La columna "Limitation relative to this work" es la que cumple el mandato del revisor de "resaltar las
innovaciones únicas" — no dejarla vacía ni genérica, cada celda debe decir algo específico y verificable contra
lo que el paper realmente hace distinto (interpretabilidad neurobiológica, tiempo real, N reales de validación
física, etc. — usar lo que ya está demostrado en el resto del paper, no inventar una ventaja no soportada por
los resultados).

## 8. Definición de "hecho" (qué se espera al final del día)

1. Escaneo de §1/§2 confirmado o corregido con hallazgos propios de Cejas (no asumir que este documento tiene
   la última palabra si encuentra algo distinto al revisar el texto de nuevo).
2. Lista de referencias nuevas candidatas, cada una con su evidencia de verificación (§4) — sección nueva
   añadida a este mismo documento.
3. Aprobación manual explícita del autor sobre esa lista, ANTES de tocar `references.bib`/`introduction.tex`.
4. `assets/references.bib` actualizado con las entradas aprobadas, en el formato de §5.
5. `sections/introduction.tex` actualizado: tabla nueva (§7, contenido real, no el esqueleto) + reformulación de
   la línea 11 sobre CPG + cualquier ajuste de prosa necesario para que fluya con lo ya existente, todo en
   `\revblue{}`.
6. Fila `R3-06` en `PROGRESS.md` actualizada de `pending` a `drafted`/`applied` según corresponda, con el patch
   correspondiente en `patches/`.
7. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` pasan antes de cualquier commit.

## 9. Explícitamente fuera de alcance / cautelas

- No tocar el párrafo de plataformas híbridas (línea 7) — no es parte de este hallazgo.
- No añadir papers "de relleno" solo para que las 3 columnas se vean parejas — una columna genuinamente más
  delgada, señalada como tal en el texto, es más honesto y más defendible ante el revisor que forzar 3 papers
  tangenciales.
- No avanzar a §5/§6 (BibTeX/integración a la escritura) sin haber completado la validación manual de §4 paso 6
  — este es un punto de parada real, no una formalidad.
- Si en el escaneo (§1) Cejas encuentra que alguna cita ya existente en `introduction.tex` tiene un problema de
  existencia/exactitud (no solo las nuevas), aplicar el mismo protocolo de §4 retroactivamente y reportarlo —
  no asumir que lo ya publicado está necesariamente verificado solo por estar ya en el repo.

---

## Referencias verificadas (Cejas añade aquí según avanza — no dejar vacío al final del día)

| Clave BibTeX propuesta | Título | Columna | DOI/URL fuente primaria | URL fuente de cruce | Nota |
|---|---|---|---|---|---|
| *(pendiente de completar)* | | | | | |
