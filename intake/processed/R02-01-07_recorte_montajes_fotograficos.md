# R02-01-07 — Recorte de los montajes fotográficos D1–D6 y E1–E6 (6→4 frames c/u) — PENDIENTE

**Estado: ✅ LISTO PARA EJECUTAR.** Plan cerrado, con selección de frames verificada visualmente (no solo por
prosa) y captions redactadas. No requiere `experiments/` ni `promote_figure.sh` — es edición pura de
`sections/results.tex`, las imágenes ya existen en `assets/` sin cambios.

**Origen:** hallazgo del informe `intake/pending/figure-redundancy-audit.pdf` (Grupo C, "Format repetition" —
"worth a look for whether all eighteen frames earn their page space"), acotado por el autor a **solo** este
grupo (el Grupo A del mismo informe se descarta por conflicto con una decisión ya ejecutada; el Grupo B queda
como backlog para la próxima ronda — ver `intake/processed/figure-redundancy-audit-triage.md`).

## 0. Criterio usado y por qué solo 2 de los 3 montajes se tocan

El informe original agrupaba los 3 montajes de 6 fotos juntos ("format repetition") sin distinguir cuáles
realmente sobran. Antes de recortar nada, se verificó **cuántos frames de cada montaje tienen una referencia
individual propia en la prosa** (no solo la figura completa) y **si hay una tabla que respalde cada frame
1:1**:

| Montaje | Frames citados individualmente en prosa | Tabla de respaldo | Veredicto |
|---|---|---|---|
| `Prueba_Terreno_Parte_1-6` (`fig:real_variable_topography_sequence`) | Los 6 — el texto narra "Frames 5–6: rolling-mode wheel slip..." y cada frame mapea 1:1 a una fila de `tab:terrain_sequence` | Sí, `tab:terrain_sequence` | **NO TOCAR — los 6 se ganan el espacio.** |
| `D1-D6` (`fig:robot-6frames`) | Solo 1 de 6 (`fig:frames-c`, citado en `results.tex:469`) | No | **Recortar a 4.** |
| `E1-E6` (`fig:RES_IMU_real`) | 0 de 6 | No | **Recortar a 4.** |

**El mínimo de 4 frames (no menos) es una restricción explícita del autor** — "no quiero que quede muy soso, o
sin partes por explicar". Con 4 frames por montaje se preserva la narrativa completa que ya está en la prosa
circundante (ver §1/§2), no es un recorte arbitrario a lo mínimo posible.

## 1. Montaje D1–D6 (`fig:robot-6frames`, "Response to Multiple Stimuli of Different Natures")

### 1.1 Inspección visual de las 6 fotos (hecha, no asumida)

Las 6 imágenes se revisaron directamente (no solo sus captions actuales):

- **D1, D2, D3** son **prácticamente idénticas** — el robot está en la misma posición, en postura cuadrúpeda,
  con solo variaciones mínimas de pose entre ellas. Esto **confirma cuantitativamente** la sospecha del informe:
  3 de los 6 frames documentan el mismo instante estático (coherente con la prosa: el robot queda "congelado" por
  el estímulo constante "Hunting Instinct" mientras las unidades $X_{15}$/$X_{16}$ se mantienen activas).
- **D4** muestra un cambio de pose sutil (una pata ligeramente levantada) — transición temprana, aún sin
  desplazamiento visible.
- **D5** muestra al robot **completamente transformado** a la configuración de rodamiento diferencial (patas
  extendidas lateralmente, terminaciones tipo rueda visibles) — sigue en la posición original, pero ya
  transformado.
- **D6** muestra al robot **desplazado significativamente** hacia el objetivo apetitivo (marcador azul/amarillo)
  — el cambio de posición más grande de las 6 fotos.

### 1.2 Selección: mantener D1, D3, D5, D6 (descartar D2 y D4)

- **D1** — representa el estado inicial (única foto necesaria para esto; D2 es redundante con D1/D3).
- **D3** — **obligatorio, es el frame referenciado por `\ref{fig:frames-c}` en `results.tex:469`** ("This state
  appears in Figure~\ref{fig:frames-c} as a period in which the robot performs no motor action").
- **D5** — el momento de transformación morfológica completa (D4 es un paso intermedio redundante con D1/D3, sin
  aportar un estado visualmente distinto).
- **D6** — el estado final, el de mayor cambio visual de las 6.

Esto preserva el arco narrativo completo que ya cuenta la prosa (`results.tex:460,469,518,520`): estado inicial
→ congelamiento indeciso (referenciado) → transformación morfológica → aproximación final y parada.

### 1.3 Nuevas captions (redactadas, listas para usar — verificar contra las fotos antes de promover, ver §4)

Reemplazan las actuales ("Frame 1 - Initial state", etc., que eran genéricas de una línea) por versiones que
consolidan el contexto que hoy solo vive disperso en la prosa circundante — reduce cuánto tiene que saltar el
lector entre figura y texto, no solo ahorra espacio:

1. **(D1) Frame 1 — Initial state:** "Initial state: the platform holds a quadrupedal stance with all three
   stimulus classes in view — the appetitive target (upper field), the near obstacle, and the more distant
   LiDAR-detected object that the network deems too far to warrant an evasive response."
2. **(D3) Frame 2 — Indecisive hold:** "Indecisive hold: the constant \emph{Hunting Instinct} stimulus keeps
   unit $X_{16}$ active and uninhibited by $X_{15}$, holding the platform stationary in quadrupedal stance until
   the aversive threat signal reaches its dispatch threshold."
3. **(D5) Frame 3 — Morphological transformation:** "Morphological transformation: following the aversive
   stimulus's peak activation ($\approx46$~s) and the resulting evasive gait dispatch, the platform reconfigures
   into differential-rolling mode."
4. **(D6) Frame 4 — Final approach:** "Final approach: after evading the aversive threat and detecting the
   appetitive target ($\approx50$~s), the platform completes an orientation correction and advances to the
   goal, coming to rest once neuron $X_{17}$ fully inhibits locomotion ($\approx90$~s)."

**No envolver en `\revblue{}` las 3 captions que ya eran correctas en sustancia (1, 3, 4) salvo que se considere
que el enriquecimiento de contenido cuenta como cambio material — sí envolver la 2, que ahora incorpora detalle
técnico ($X_{15}$/$X_{16}$) que antes no estaba en la caption.** Criterio a confirmar con el bot de redacción
al ejecutar (regla del proyecto: "default to wrapping" ante la duda).

## 2. Montaje E1–E6 (`fig:RES_IMU_real`, "Response to Variable Topographies" — terreno irregular)

### 2.1 Inspección visual de las 6 fotos (hecha, no asumida)

A diferencia de D1-D6, estas 6 fotos **sí muestran una progresión continua** — el robot avanza visiblemente de
derecha a izquierda a través del tapete de cartón arrugado en cada frame sucesivo (no hay duplicados exactos
como en D1-D3). Aun así, 2 de los 6 son puntos intermedios que no añaden un estado narrativamente distinto de
sus vecinos inmediatos:

- **E1** — entrando al terreno, borde derecho.
- **E2** — avanzando sobre el terreno, de frente a cámara (redundante con E1/E3 — mismo tipo de información,
  "todavía atravesando", sin un evento nuevo que marcar).
- **E3** — en el punto de mayor relieve del terreno, postura cuadrúpeda clara y de cerca — coincide con el
  momento que la prosa describe como la transformación a modo cuadrúpedo tras la señal de estancamiento.
- **E4** — continúa el cruce, más a la izquierda (redundante con E3/E5 — mismo tipo de información que E3, sin
  evento nuevo).
- **E5** — acercándose al borde izquierdo, a punto de salir del terreno.
- **E6** — fuera del terreno, sobre piso plano — estado final.

### 2.2 Selección: mantener E1, E3, E5, E6 (descartar E2 y E4)

Cubre, con espaciado razonable, los 4 eventos que la prosa (`results.tex:576`) sí puntualiza con tiempos
concretos: entrada (t≈0s, superficie con variación <1.2cm) → transformación a modo cuadrúpedo tras la señal de
estancamiento (~t=13-23s) → tramo final de cruce → recuperación a modo de rodamiento diferencial (~t=86s, cuando
cesa la actividad de $X_0$).

### 2.3 Nuevas captions (redactadas, listas para usar — verificar contra las fotos antes de promover, ver §4)

1. **(E1) Frame 1 — Entering the terrain:** "Entering the terrain: the platform advances onto the irregular
   surface (height variance below 1.2~cm), a region it clears within the first $\approx13$~s in its initial
   locomotion mode."
2. **(E3) Frame 2 — Quadrupedal transformation:** "Quadrupedal transformation: once the stagnation signal
   reaches its maximum sustained amplitude, the network commits to the quadrupedal gait to negotiate the
   roughest section of the mat."
3. **(E5) Frame 3 — Approaching the exit:** "Approaching the exit: the platform sustains ground clearance in
   quadrupedal mode across the highest-relief sections, nearing the mat's far edge."
4. **(E6) Frame 4 — Recovery:** "Recovery: around $t\approx86$~s, once unit $X_0$'s activity ceases (Figure~
   \ref{fig:NEU_IMU_real}), the platform exits the rough section and reverts to differential-rolling mode,
   completing the crossing."

**Nota de cautela explícita para quien ejecute:** a diferencia de D1-D6, no fue posible confirmar con certeza
desde las fotos (vista superior/lateral) el modo exacto de locomoción (patas vs. ruedas) en cada frame
específico — las captions de arriba se apoyan en los tiempos y eventos que la prosa ya afirma, no en una
lectura visual del modo. **Verificar contra las 6 fotos originales antes de finalizar** (§4) — si alguna
caption resulta inconsistente con lo que la foto realmente muestra, ajustarla, no forzarla a calzar con el
texto.

## 3. Referencias cruzadas — qué cambia y qué no

- `\ref{fig:frames-c}` (`results.tex:469`, apunta a D3, ahora 2do subfigure de 4): **no requiere edición** — con
  `subcaption`, `\ref{}` a un `\label{}` dentro de un `subfigure` resuelve dinámicamente la letra según la
  posición actual tras recompilar (pasará de mostrar "(c)" a "(b)" automáticamente). Confirmar esto en la
  compilación de prueba (§4), no asumirlo ciegamente.
- `\label{fig:robot-6frames}` y `\label{fig:RES_IMU_real}` (las figuras completas): sin cambio, siguen
  apuntando a la misma figura, solo con menos subfiguras adentro.
- Los `\label{}` individuales de los 4 frames que se mantienen (`fig:frames-a`, `fig:frames-c`, `fig:frames-e`,
  `fig:frames-f` para D; `fig:frames-a2`, `fig:frames-c2`, `fig:frames-e2`, `fig:frames-f2` para E) **se
  conservan tal cual** — no renombrar, aunque ahora ocupen posiciones 1-4 en vez de 1,3,5,6. Los de D2/D4/E2/E4
  (`fig:frames-b`, `fig:frames-d`, `fig:frames-b2`, `fig:frames-d2`) se eliminan junto con sus subfigures — **grep
  `sections/*.tex` para confirmar que ninguno se cita en otro punto del documento antes de borrarlos.**

## 4. Layout — de 3+3 a 2+2

Con 4 subfiguras en vez de 6, usar una rejilla 2×2 (dos por fila) en vez de 3+3 — imágenes más grandes y
legibles, consistente con el estilo que ya usan otros bloques de 2 paneles del documento:

```latex
\begin{figure}[t]
  \centering
  \begin{subfigure}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth]{D1.png}
    \caption{<texto de §1.3, frame 1>}
    \label{fig:frames-a}
  \end{subfigure}\hfill
  \begin{subfigure}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth]{D3.png}
    \caption{<texto de §1.3, frame 2>}
    \label{fig:frames-c}
  \end{subfigure}

  \vspace{0.6em}

  \begin{subfigure}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth]{D5.png}
    \caption{<texto de §1.3, frame 3>}
    \label{fig:frames-e}
  \end{subfigure}\hfill
  \begin{subfigure}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth]{D6.png}
    \caption{<texto de §1.3, frame 4>}
    \label{fig:frames-f}
  \end{subfigure}
  \caption{Four representative frames from the real-robot experiment facing visual stimuli of different nature:
  (a)–(d) show the temporal evolution across the trial.}
  \label{fig:robot-6frames}
\end{figure}
```

Mismo patrón para `fig:RES_IMU_real` con E1/E3/E5/E6 y las captions de §2.3. Actualizar el texto del `\caption{}`
externo de "(a)–(f)" a "(a)–(d)" en ambos casos.

## 5. Pasos para ejecutar

1. Editar `sections/results.tex`: aplicar el layout de §4 a los dos bloques (D-montage ~línea 471-516,
   E-montage ~línea 581-619 — confirmar número exacto antes de editar, puede haber corrido).
2. `grep -n "fig:frames-b\b\|fig:frames-d\b\|fig:frames-b2\|fig:frames-d2"` sobre `sections/*.tex` para confirmar
   que los 4 labels que se eliminan (D2, D4, E2, E4) no se citan en ningún otro punto — si alguno aparece,
   detenerse y decidir antes de borrar.
3. Antes de dar por buenas las captions de §1.3/§2.3, **abrir D1/D3/D5/D6 y E1/E3/E5/E6 directamente** (no solo
   confiar en este documento) y confirmar que cada caption describe lo que la foto realmente muestra —
   particularmente la nota de cautela de §2.3 sobre el modo de locomoción en el montaje E.
4. Compilar (`scripts/compile_pdf.sh` si está disponible, o al menos `scripts/validate_tex.sh`) y verificar
   visualmente que `\ref{fig:frames-c}` en el párrafo de `results.tex:469` efectivamente imprime "(b)" tras el
   recorte (confirma que la re-letra dinámica de `subcaption` funcionó como se espera).
5. Envolver en `\revblue{}` las captions que incorporan contenido nuevo (ver nota de §1.3) — las imágenes en sí
   no cambian, así que esto es puramente textual.
6. `PROGRESS.md`: nueva fila `C-xx` (`scripts/next_id.sh C`), `Category: Escritura`, sin `Data source` (no hay
   experimento nuevo, las imágenes ya existían en `assets/`), `Target section(s): results.tex (fig:robot-6frames,
   fig:RES_IMU_real)`.
7. `scripts/validate_tex.sh`/`scripts/check_roundtrip.sh` antes de cualquier commit.

**Nota: `D2.png`, `D4.png`, `E2.png`, `E4.png` se quedan en `assets/` sin usar tras esto (no se borran del
repo).** A diferencia de una figura reemplazada, retirar un subfigure de un montaje no es una promoción con
`--force` — no hay una "versión anterior" que limpiar, solo se deja de incluir el archivo en `results.tex`. Si
se quiere limpiar `assets/` de archivos huérfanos, es una decisión aparte, no parte de este bloque.
