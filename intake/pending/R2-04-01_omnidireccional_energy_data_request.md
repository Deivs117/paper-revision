# R2-04-01 — Solicitud de datos: consumo energético en Modo Omnidireccional (X)

**Estado: 🔲 PENDIENTE (bloqueado por datos externos, no es una tarea ejecutable hoy en este repo).**

**Origen:** `intake/processed/R02-01-03_energia_transicion_y_modo_R2-04.md` §5 y
`experiments/R2-04-mode-energy/README.md` — la fila Omnidireccional de `tab:mode_steady_state_energy` en
`results.tex` es un placeholder N=1 (5.71 W, sin SD, sin réplica). Este documento es la lista de tareas a
entregar al equipo de hardware para reemplazarla por un dato real.

## Contexto para el equipo de hardware

La tabla de consumo por modo en el paper ya tiene datos reales y replicados para Cuadrúpedo (N=20,
1.94 ± 1.77 W) y Diferencial (N=20, 1.36 ± 0.98 W). Falta el mismo tipo de dato para el modo Omnidireccional:
hoy solo existe **un** segmento de 38.6s, sin repetición, que no permite calcular una desviación estándar ni
defender el número ante los revisores.

## Lista de tareas para tomar los datos

1. **Diseñar y ejecutar una campaña de pruebas dedicada en Modo Omnidireccional (X)**, con **N ≥ varias corridas
   independientes** (referencia: N=20 en los modos ya medidos; cuantas más corridas, mejor calidad estadística).
2. **Registrar cada corrida con el mismo esquema de CSV** que las carpetas ya usadas para C/H en
   `experiments/real/`:
   - Columna `robot_cmd` con el comando estructural `x` marcando la entrada al modo Omnidireccional (igual
     convención que `c`→Cuadrúpedo, `z`→Diferencial).
   - Columna `current_A` con la corriente medida de forma fiable (no usar las columnas `power_W`/`voltage_V`
     originales — están rotas, con magnitud implausible, y ya descartadas en todo el pipeline).
3. **Verificar/reportar si existe una ventana de acoplamiento electromecánico medible al entrar en modo X**
   (transición mecánica al inicio de la corrida). Hoy no hay ninguna calibrada para `x` (sí para `z`=2.92s y
   `c`=1.56s), así que el segmento completo se usa sin recortar. Si el equipo de hardware puede medir/estimar
   esa ventana para X, se puede incorporar; si no, confirmar explícitamente que debe seguir tratándose como
   "segmento completo sin recorte".
4. **Etiquetar la condición física de cada corrida** (piso plano, rampa, ensayo estático, u otra) desde el
   diseño del experimento. En C/H se detectó que mezclar condiciones distintas dentro del mismo modo infla la
   varianza intra-modo — sería mejor evitar ese problema en X desde el inicio, o al menos dejarlo etiquetado
   para poder controlarlo en el análisis.
5. **Entregar los datos como carpeta(s) nueva(s) dentro de `experiments/real/`**, mismo directorio que usan las
   corridas actuales de C/H, para que el script existente pueda re-correrse sin cambios de formato.

## Qué pasa una vez lleguen los datos (no es tarea del equipo de hardware, informativo)

- Se re-corre `experiments/R2-04-mode-energy/scripts/build_mode_energy.py` contra la(s) carpeta(s) nueva(s).
- Se actualiza solo la fila X de `tab:mode_steady_state_energy` (media ± SD / N) — nada más del pipeline cambia.
- El seguimiento de este bloqueo ya está trazado en `PROGRESS.md` (fila `R2-04`, estado `drafted`) y en
  `experiments/R2-04-mode-energy/README.md` — esos dos archivos son la fuente de verdad de cuándo/cómo actuar
  cuando los datos lleguen.
