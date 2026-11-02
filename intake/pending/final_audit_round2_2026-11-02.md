# Auditoría final multi-autor — ronda 2, antes del envío (2026-11-02)

**Estado: 🟢 lista para ejecutar.** Los 11 ítems de los revisores están `synced-to-overleaf`, no hay
filas abiertas y el PDF compila (104 páginas, 0 errores). Este es el último filtro antes de enviar.

Réplica de `intake/processed/redundancy_closing_audit.md` (la auditoría de 4 autores de la ronda 1,
que produjo los cuatro `final_audit_*.md` de septiembre), **con las mejoras que esa corrida enseñó**.
Lee la sección 7 si quieres saber qué cambió respecto a aquella.

## 0. Cómo se ejecuta

Cuatro sesiones independientes de Claude Code, **una por autor**: Diego, Sebas, Samuel y Deivi. Cada
uno corre esta misma tarea completa en su propia sesión. No se reparten el paper: los cuatro lo leen
entero. El solape es deseable, porque un hallazgo que encuentran dos es un hallazgo confirmado.

**Esta pasada es de HALLAZGOS, no de corrección.** Nadie edita `sections/*.tex`. Cada sesión escribe
su propio archivo en `intake/pending/` (sección 5). La consolidación va aparte, después.

Antes de empezar: `git pull origin main`.

## 1. Qué se busca — seis categorías

Las cuatro de la ronda 1, más dos que esta ronda demostró que hacían falta.

### 1.1 Inconsistencias de datos
Cifras que se contradicen entre sí, o que contradicen los datos crudos de `experiments/`.
**Esta es la categoría de mayor rendimiento: los tres peores problemas de la ronda salieron de aquí.**
Ejemplos reales ya resueltos, por si sirven de patrón:
- `C-69`: la prosa decía Roll RMS ≤1.59° y `tab:fsm_comparison` reportaba 6.751° para el mismo
  escenario. Causa: **dos baterías distintas del mismo experimento** citadas como si fueran una.
- `C-74`: las tablas usaban desviación **poblacional** en dos sitios y **muestral** en otro, sin
  declararlo. Se detectó porque el cociente daba exactamente √(14/15).
- Appetitive físico: el caption dice "three hardware replicates" y hay **cuatro** ensayos con dato
  válido. **Sigue abierto, es una decisión del autor, no lo reportes otra vez como hallazgo nuevo.**

### 1.2 Redundancia y contenido duplicado
Definiciones de métrica restablecidas en varios sitios, descripciones repetidas, figuras casi
idénticas entre simulación y físico. Ya se hicieron varias pasadas (`R2-01`, `R3b-01`, `C-60`,
`C-64`, `C-66`, `C-67`), así que lo que quede será sutil: busca sobre todo **redundancia entre texto
viejo y texto nuevo**, que es la que sobrevive a las pasadas anteriores.

### 1.3 Candidatos a acortar
Tablas o figuras condensables **sin perder validez estadística ni capacidad de comunicar**. Propón
el cómo concreto (fusionar dos tablas, columnas redundantes, tabla dispersa → figura), no solo "es
largo".

### 1.4 Ortografía y convenciones académicas
Inglés académico: tipografía, concordancia, puntuación, un mismo término para un mismo concepto en
todo el documento. Mayúsculas consistentes en títulos, notación matemática coherente, formato de
citas.

### 1.5 🆕 Calcos del español e inglés no idiomático
**El paper lo escribimos hispanohablantes y esta categoría no existía en la ronda 1.** Busca:
- Falsos amigos: *actually* por "actualmente", *realize* por "realizar", *eventually* por
  "eventualmente", *assist* por "asistir a", *sensible* por "sensato", *library* por "librería".
- Calcos de estructura: *"the same"* donde el inglés pide *"it"*; *"permit to"* por *"allow to"*;
  *"in base to"*, *"according to the literature"* usado como muletilla; *"the robot presents a
  behavior"* por *"the robot behaves"*.
- Gerundios encadenados donde el inglés usaría una oración de relativo.
- Orden adjetivo-sustantivo invertido, artículos sobrantes (*"the Figure 3 shows"*).
- Voz pasiva excesiva donde la activa es más natural y más corta.
No es una reescritura de estilo: son errores concretos y localizables.

### 1.6 🆕 Texto tocado en las últimas 48 horas
Es el que menos ojos ha tenido. Repásalo con atención específica:
- `C-76` (hoy): se quitaron **63 em dashes** y se repuntuó o reescribió cada frase. **Verifica que
  ninguna quedó ambigua, con puntuación doble, o con el sentido cambiado.** Es el cambio más
  extenso y más reciente.
- `C-66`, `C-67`: consolidaciones de redundancia en `results.tex`.
- `C-73`: marcas "Simulation data." / "Physical-robot data." añadidas a 16 captions.
- `C-70`–`C-72`, `C-75`: 25 figuras regeneradas. Mira las **figuras**, no solo el texto: leyendas
  tapadas, ejes, unidades, etiquetas ilegibles.

## 2. 🆕 Verifica contra los datos, no solo leyendo

La lección más importante de esta ronda: **los hallazgos que valieron algo salieron de recomputar,
no de leer.** Pero ojo con qué datos tienes: **no todo `experiments/` está versionado.**

### Lo que SÍ puedes recomputar (está en el repo, te llega con `git pull`)

| Fuente | Qué respalda |
|---|---|
| `experiments/simulation/*/test_*/trial_summary.json` (96 ensayos) | `tab:consolidated_simulation_metrics` y las 4 filas de suite de `tab:fsm_comparison` |
| `experiments/real/` (56 ficheros) | las tablas y figuras del robot físico |
| `experiments/R3-05-inspection/data/` (101 ficheros) | `tab:inspection_metrics` y la tarea de inspección |
| `experiments/_plotting/vectorized/*.csv` | los rasters de neuronas y las series IMU |
| `experiments/R2-02-fsm-baseline/output/table_master_comparison.csv` | los agregados de `tab:fsm_comparison` |

```
cd paper-revision
experiments/.venv_plotting/bin/python      # trae numpy/pandas/matplotlib
```
Si no tienes el venv: `cd experiments && uv venv .venv_plotting && uv pip install numpy pandas matplotlib`.

### Lo que NO tienes (gitignored, solo en la máquina de Deivi)

- `experiments/R3-04-noise-robustness/data/` — batería de perturbación combinada y familias de
  terreno C1/C2.
- `experiments/R2-02-fsm-baseline/data/` — los ensayos crudos del FSM.

La regla es `experiments/*/data/`; por eso `simulation/` y `real/` sí están (cuelgan directamente de
`experiments/`) y estas dos no. **Si tu duda cae sobre una cifra que sale de ahí, repórtala igual**,
marcada como *"requiere verificación con datos no versionados"*, y Deivi la recomputa. No la
descartes por no poder comprobarla: el problema del Roll RMS (`C-69`) vivía justo en una de esas
dos carpetas.

⚠️ **Trampa documentada:** hay familias con el mismo nombre en carpetas distintas
(`experiments/simulation/familia_c2_pendiente` ≠
`experiments/R3-04-noise-robustness/data/familia_c2_pendiente`) y **no contienen lo mismo**. Lee el
`README.md` del experimento antes de recomputar nada suyo.

Cada hallazgo de la categoría 1.1 debe decir **cómo lo verificaste**. "Me parece inconsistente" no
es un hallazgo; "recomputé X desde Y y da Z, el paper dice W" sí lo es. Si no pudiste verificarlo,
dilo con esas palabras.

## 3. 🆕 Lo que NO es un hallazgo

Para no gastar tiempo ni reabrir debates cerrados:
- **Los en dash `--`**: `Naka--Rushton`, `Mann--Whitney`, `$0.2$--$0.7$`, `levels 0--4`,
  `Writing--original draft`, `(a)--(c)`. Son tipografía correcta. Hay 46 y se quedan.
- **Nombres internos dentro de `\label{}`, `\ref{}` y `\includegraphics{}`** (`fig:failure_by_family`,
  `NEU_EST_UNIG.png`): no se imprimen en el PDF. Solo importa el texto visible.
- **Tamaño, escala y ubicación de las figuras en la página**: lo decide la editorial en producción.
  Nosotros solo garantizamos que la tipografía propia de cada figura sea legible.
- **Los 15 `---` de `preamble.tex`**: son reglas de comentario de la plantilla de Elsevier.
- **Las dos baterías de terreno citadas por separado** (`C-69`): es deliberado y está documentado.
- **La SD poblacional declarada** (`C-74`): el autor eligió declararla, no unificarla. Si crees que
  hay que unificar, dilo como recomendación, no como error nuevo.
- **El PDF de 36 MB**: el manuscrito ya pasó dos envíos así.

## 4. 🆕 Prioriza cada hallazgo

Etiqueta cada uno, con este criterio:
- **Alta** — un revisor lo leería como error factual, contradicción o dato que no cuadra. Bloquea el
  envío.
- **Media** — debilita el argumento, confunde, o es redundancia visible. Debería corregirse.
- **Baja** — estilo, fluidez, preferencia. Se corrige si hay tiempo.

Si no encuentras nada en una categoría, **dilo explícitamente** ("1.3 — sin hallazgos") en vez de
omitirla: así la consolidación sabe que sí se revisó.

## 5. Entregable

**No edites `sections/*.tex`.** Escribe un archivo nuevo:

```
intake/pending/final_audit_r2_<autor>_2026-11-XX.md
```

con `<autor>` ∈ {`diego`, `sebas`, `samuel`, `deivi`} y la fecha real. Una sección por categoría
(1.1–1.6). Cada hallazgo:

- **Ubicación exacta**: archivo + línea, o el `\label{}` más cercano.
- **Prioridad**: alta / media / baja.
- **Descripción concreta** del problema.
- **Cómo lo verificaste** (obligatorio en 1.1).
- **Corrección sugerida**, sin aplicarla.

## 6. 🆕 Orden de lectura — distinto para cada autor

En la ronda 1 los cuatro leyeron en el mismo orden, así que la fatiga caía siempre en las mismas
secciones finales. Empieza por la tuya y sigue en círculo:

| Autor | Empieza por |
|---|---|
| Deivi | `results.tex` (§ ablación, FSM, inspección) |
| Diego | `methodology.tex` |
| Sebas | `introduction.tex` + `conclusions.tex` |
| Samuel | `results.tex` (§ físico, energía, MLP) |

Después de tu sección de arranque, lee **las seis completas** igualmente. El orden solo reparte en
qué llegas con la vista fresca.

`scripts/check_word_growth.sh` ayuda a priorizar qué releer primero; no sustituye la relectura.

## 7. Qué cambió respecto a la auditoría de la ronda 1

1. Dos categorías nuevas: calcos del español (1.5) y texto recién tocado (1.6).
2. Verificación contra datos crudos obligatoria en 1.1, con la trampa de las familias homónimas
   documentada.
3. Lista explícita de no-hallazgos (sección 3), para no reabrir lo cerrado.
4. Prioridad obligatoria por hallazgo (sección 4).
5. Orden de lectura rotado por autor (sección 6).
6. "Cómo lo verificaste" como campo obligatorio del entregable.

## 8. Consolidación (sesión aparte, cuando existan los 4 archivos)

1. Cruzar los 4, agrupar duplicados. Un hallazgo que encuentran dos o más sube de prioridad.
2. Un patch por hallazgo real confirmado, en `\revblue{}` solo si cambia contenido.
3. Fila `C-xx` por patch (`scripts/next_id.sh C`), `Category: Escritura`, citando los documentos de
   origen.
4. **Compilar** (`scripts/compile_pdf.sh`) antes de cualquier commit, no solo `validate_tex.sh`:
   esta ronda hubo un error de LaTeX que `validate_tex.sh` dio por bueno porque solo comprueba
   balance de llaves.
5. Mover los 4 archivos a `intake/processed/` solo cuando sus filas lleguen a `applied`.
6. Push a Overleaf al final (solo Deivi tiene el token), y **`git push origin main` aparte**: el
   script de sync no sube a GitHub.
