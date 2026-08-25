# Resumen del sistema (para entendimiento general)

> Este documento es un resumen en español, pensado para que cualquier persona (tú, un coautor, un
> agente nuevo) entienda rápido qué es este repositorio y cómo funciona, sin tener que leer todo
> el detalle técnico. **La fuente de verdad técnica sigue siendo `README.md` (en inglés)** — este
> documento no la reemplaza, y puede quedar desactualizado en detalles finos si `README.md`
> cambia y este no se actualiza a la par.

## ¿Qué es esto?

Este repositorio (`paper-revision`) existe para gestionar la revisión mayor del manuscrito
**ROBOT-D-26-00122R1** para la revista *Robotics and Autonomous Systems*, con fecha límite de
reenvío el **31 de agosto de 2026**.

El manuscrito completo vive como un solo archivo `.tex` en Overleaf, donde los coautores editan
desde el navegador. Este repo agrega, por encima de eso, control de versiones con git y un flujo
para que un agente de IA (o tú mismo) convierta los pedidos de los revisores en cambios de texto
LaTeX concretos, sin depender de copiar y pegar manualmente entre Overleaf y un editor de texto.

## Las tres carpetas involucradas

```
~/Documents/Paper/
├── paper-revision/              ← este repo. Aquí pasa TODO el trabajo real.
├── 6a23870b4fcac02449561a35/    ← clon de Overleaf. Solo sincronización, nunca se edita a mano.
└── PETER_SIMULATION/            ← repo de tus compañeros (firmware/ROS2). Solo lectura, como
                                    material de referencia para escribir contenido nuevo.
```

## El flujo, en una imagen simple

```
   Overleaf (editado por coautores)
            │
            │  scripts/pull_from_overleaf.sh
            ▼
   source/main_monolithic.tex  ──se divide en──▶  sections/*.tex
   assets/ (imágenes, .bib, .cls)                  (una por sección: introduction.tex,
                                                      methodology.tex, results.tex,
                                                      conclusions.tex)
            │
            │  se edita la sección puntual que corresponde
            │  al pedido del revisor (o al contenido nuevo)
            ▼
   sections/*.tex modificado
            │
            │  scripts/reassemble.py + scripts/validate_tex.sh
            ▼
   source/main_monolithic.tex reconstruido
            │
            │  scripts/push_to_overleaf.sh  (con guardas de seguridad)
            ▼
   Overleaf actualizado — los coautores lo ven en el navegador
```

**Por qué se divide en `sections/`:** para que un agente que necesita hacer un cambio puntual
(por ejemplo, en Resultados) no tenga que leer el manuscrito completo cada vez — eso ahorra
tokens/costo y hace el trabajo más rápido y repetible.

## Las dos guardas de seguridad (ya probadas, no solo diseñadas)

1. **Antes de traer cambios de Overleaf** (`pull`): si tienes trabajo local sin empujar todavía,
   el sistema **se niega a hacer el pull** — para no sobreescribir silenciosamente tu trabajo.
2. **Antes de mandar cambios a Overleaf** (`push`): si un coautor editó algo en Overleaf mientras
   tú trabajabas, el sistema **se niega a empujar** — para no pisar la edición de otra persona.
   Nunca hay "merge" automático; si hay conflicto, te avisa y decides tú.

Ambas guardas fueron probadas con casos reales de conflicto (no solo en teoría) el 24 de agosto.

## `PROGRESS.md` — el tablero de todo lo pendiente

Un solo archivo con una fila por cada cambio pendiente, venga de donde venga:

- `R2-xx` / `R3-xx` — pedidos de los revisores 2 y 3 (10 ítems en total).
- `N-xx` — contenido nuevo que tú aportas (por ejemplo, redactar sobre un sistema que documentó
  un compañero).
- `C-xx` — correcciones sueltas que no vienen de un revisor.

Cada fila tiene un estado: `pending` → `drafted` → `applied` → `synced-to-overleaf`.

## `intake/` — cómo metes información cruda al sistema

Si tienes un documento markdown (de un compañero, tuyo, sobre un hallazgo de
`PETER_SIMULATION`), lo dejas en `intake/pending/`. El agente lo lee, decide en qué sección del
paper encaja, y crea las filas correspondientes en `PROGRESS.md`. De ahí en adelante sigue el
mismo camino que cualquier otro cambio.

## `experiments/` — cómo entran figuras/datos que todavía no existen

Varios ítems grandes del checklist (R3-01 ablación, R3-04 robustez a ruido, R3-05 métricas de
inspección) no piden solo redactar texto: piden una figura o número que **todavía no existe**, y
que probablemente sale de correr simulaciones (a veces usando `PETER_SIMULATION` como referencia)
o de reprocesar datos del robot físico.

Para eso existe `experiments/<ID>-<slug>/` (mismo ID que la fila de `PROGRESS.md`, p. ej.
`experiments/R3-01-basal-ganglia-ablation/`):

- `README.md` — qué produce, con qué parámetros/semilla, de dónde salen los datos (si depende de
  `PETER_SIMULATION`, se anota el commit exacto usado, porque ese repo sigue cambiando por su
  cuenta), y cómo volver a generarlo.
- `scripts/` — el código que genera la figura. Aquí sí se permite usar numpy/matplotlib/pandas/
  ROS 2, a diferencia del resto de `scripts/` que es solo bash/Python estándar.
- `data/` — salida cruda (rosbags, logs, video). **No se versiona en git** — se regenera corriendo
  el script de nuevo.
- `output/` — el resultado final ya procesado (CSVs pequeños, la figura misma). **Sí se versiona.**

Cuando la figura está lista, `scripts/promote_figure.sh` la copia de `output/` hacia `assets/` en
la ruta exacta que va a usar el LaTeX (se niega a sobreescribir algo que ya exista salvo que se
use `--force`). De ahí en adelante es un parche normal: se referencia la imagen en `sections/`, se
redacta el texto, y se sincroniza con Overleaf como cualquier otro cambio.

## Huecos menores ya resueltos (25 de agosto)

Cuatro huecos de diseño de bajo riesgo (dado que tú eres quien más escribe) pero reales, resueltos
con scripts livianos que **avisan, no bloquean**, salvo el hook de commit:

- **Referencias cruzadas tipo "Section 2" escritas a mano** (no `\ref{}`): `scripts/
  check_hardcoded_refs.sh` las detecta (ya encontró 4 instancias reales) y se corre automáticamente
  cada vez que haces `push_to_overleaf.sh` — solo avisa, nunca bloquea el push, porque un script no
  puede saber con certeza si el número sigue siendo correcto.
- **Nada forzaba correr `validate_tex.sh`/`check_roundtrip.sh` antes de cada commit**: ahora existe
  un hook de git (`scripts/install_hooks.sh`, una vez por clon) que se activa solo cuando el commit
  toca `sections/` o `source/`, regenera `source/main_monolithic.tex` automáticamente, y bloquea el
  commit si algo queda mal. Probado con un caso real que rompe el LaTeX (bloqueado correctamente) y
  uno válido (pasa y queda commiteado).
- **Asignar IDs `N-xx`/`C-xx` a mano**: `scripts/next_id.sh N` o `scripts/next_id.sh C` calcula el
  siguiente disponible automáticamente.
- **Dos parches tocando la misma sección a la vez**: `scripts/check_target_conflicts.sh <slug>`
  avisa si otra fila de `PROGRESS.md` ya apunta al mismo archivo. No es un candado real — con un
  solo escritor principal, la solución práctica sigue siendo terminar y commitear uno antes de
  empezar el otro.

## `OUTLINE.md` — el mapa barato del paper

Un archivo corto que resume qué trata cada sección, términos clave, y qué referencias cruzadas
hay entre secciones. El agente lo lee siempre antes de tocar una sección puntual, para tener
contexto global sin tener que leer el manuscrito completo.

## Estado actual (al 25 de agosto de 2026)

- El pipeline completo está **implementado y probado** contra el manuscrito real: primer `pull`
  exitoso trajo las 4 secciones (`introduction`, `methodology`, `results`, `conclusions`), ~90
  imágenes, la bibliografía y la plantilla de la revista.
- Se diseñó e implementó `experiments/` (25 de agosto) — la laguna de "cómo entran figuras/datos
  que todavía no existen" ya está cerrada: `scripts/promote_figure.sh` probado con casos de éxito
  y de rechazo (no sobreescribe sin `--force`, no acepta archivos fuera de `output/`). `PROGRESS.md`
  tiene ahora una columna `Data source` marcando qué ítems del checklist necesitan esto (R3-01,
  R3-02, R3-05 confirmados; R2-02, R2-04, R3-03, R3-04 posibles según se verifiquen los huecos).
- Los cuatro huecos menores identificados el mismo día (referencias hardcodeadas, sin hook de
  pre-commit, asignación manual de IDs, sin aviso de conflicto entre parches) también quedaron
  resueltos — ver sección arriba.
- Se hizo una lectura completa de `introduction.tex`, `results.tex`, `conclusions.tex` y, el 25 de
  agosto, también `methodology.tex` (501 líneas). Hallazgos importantes ya registrados en
  `PROGRESS.md`/`OUTLINE.md`:
  - **R3-06** (tabla comparativa de literatura) es más barato de lo esperado: la comparación ya
    existe como texto narrativo en la introducción, probablemente solo falta convertirla a tabla.
  - **R2-03** (consolidar limitaciones) es más complejo de lo esperado: hay **dos** discusiones
    de limitaciones separadas (una en Resultados, otra en Conclusiones) que hay que fusionar, no
    una sola que mover.
  - **R2-04** (overhead de cómputo del MLP) está **parcialmente resuelto ya** — la comparación de
    latencia del MLP contra otros clasificadores ya existe en Resultados.
  - **R3-01/R3-02** (ablación de la red basal ganglia / WTA vs threshold) son **huecos reales**,
    confirmado ahora con lectura completa de `methodology.tex` — no existe ablación ni comparación
    formal todavía. Sí hay material reutilizable: un párrafo `\revblue{}` ya escrito (justifica la
    arquitectura citando literatura y una latencia de decisión de ~47ms) y el hecho de que el
    módulo de locomoción ya usa lógica de umbral explícito (20°, `Ar=28.0`) en otra parte del
    circuito — un punto de contraste natural para la comparación WTA-vs-umbral. Sigue siendo el
    trabajo más grande y de mayor prioridad para el Revisor 3.
  - Se encontró una **inconsistencia real** en el texto: Conclusiones dice que las métricas del
    MLP "no fueron evaluadas", pero Resultados ya las tiene — registrado como `C-01`.

## Para el detalle técnico completo

- `README.md` — arquitectura completa, especificación exacta de cada script, formatos de archivo.
- `CLAUDE.md` — reglas duras para cualquier agente que trabaje en este repo.
