# C-19 — Limpieza de layout: Tabla 1, Tabla 10, Figs. 43-46/55-58/59 — CERRADO

**Estado (2026-08-29): ✅ Ejecutado, commiteado (`84a07c4`), pendiente de sync a Overleaf.**

**Origen:** el autor compartió 8 capturas de pantalla del PDF compilado señalando tablas/figuras que
se veían mal (desbordadas, con espacio muerto, o demasiado grandes para lo que aportan) y pidió
arreglarlas, con preguntas de por medio antes de tocar nada.

## 1. Diagnóstico por elemento

| Elemento | Síntoma reportado | Causa raíz encontrada |
|---|---|---|
| Tabla 1 (`table:action_selection_comparison`, introduction.tex) | Se veía un "59" flotando dentro de la tabla | 6 columnas fijas sumaban 14.4cm; la fila de "Basal ganglia (this work)" con 7 citas apiladas hacía la fila tan alta que la tabla se corría más allá de una página, y el número de página del pie ("59") quedaba visualmente superpuesto |
| Tabla 10 (`tab:terrain_sequence`, results.tex) | Columna "Trigger / mechanism" con una palabra por línea, tabla altísima | Columnas "Terrain segment"/"Mode" definidas como `l` (ancho natural, sin ajuste de línea) le robaban casi todo el ancho de página a la única columna flexible (`X`) |
| Figs. 55–58 (Appetitive/Aversive/Complex/Obstacle Real, results.tex) | "Espacio muerto" entre los paneles (a) y (b) de cada figura | Ambos subfigures declarados a `0.32\textwidth` (64% del ancho total), dejando el 36% restante como un único hueco `\hfill` en el medio |
| Figs. 43–46 (confusion matrix/ROC/training loss/architecture ablation, results.tex) | 4 figuras completas, muy grandes para lo poco que aportan cada una | Cada gráfico (matriz 2×2, curva ROC, curva de entrenamiento, barras de ablation) vivía en su propio `figure` a ancho completo — 4 floats separados para un solo tema (evaluación del MLP) |
| Fig. 59 (`fig:MorphologicalEnergy`, results.tex) | Demasiado grande para 2 barras con error bars | Ancho fijo a `0.75\textwidth` sin razón de contenido |

## 2. Decisiones tomadas (con el autor, antes de ejecutar)

- Tabla 1: reequilibrar anchos (12.4cm total) + `\footnotesize`, **sin** recortar la lista de citas.
- Tabla 10: convertir las 4 columnas a anchos que ajustan línea — arreglo puramente mecánico.
- Figs. 55–58: **ninguna se elimina** — el autor fue explícito en esto. Solo se ensanchan ambos
  paneles a `0.48\textwidth` para cerrar el hueco central.
- Figs. 43–46: fusionar en una sola figura 2×2 (`fig:mlp_eval_grid`), reutilizando los 4 PNG
  existentes sin regenerarlos — reescritura de los 3 párrafos que las citaban, apuntando a
  `\ref{fig:mlp_eval_grid}a`–`d` en vez de a 4 labels separados.
- Fig. 59: sin vecina natural para agrupar — solo achicar a `0.5\textwidth`.

## 3. Ejecución

Todos los cambios son de layout/LaTeX puro — ningún número, cita o conclusión cambió. Los 3
párrafos reescritos para citar `fig:mlp_eval_grid` van en `\revblue{}` (contenido de esta ronda).
Verificado visualmente página por página en el PDF compilado antes de commitear.

**Incidente de concurrencia (documentado para que no se repita):** las primeras 4 correcciones se
perdieron dos veces durante la ejecución porque `scripts/check_roundtrip.sh` corrió `split_sections.py`
contra un `source/main_monolithic.tex` desactualizado justo cuando otra sesión (cerrando `N-09`,
commit `f27ff12`) commiteaba en paralelo — el `split` regeneró `sections/` desde el monolito viejo,
revirtiendo mis ediciones aún no reflejadas allí. Se recuperó ambas veces comparando contra lo
esperado y reaplicando; a partir de ahí se corrió `scripts/reassemble.py` inmediatamente después de
cada edición, antes de cualquier `validate`/`check_roundtrip`, para evitar un tercer choque.

## 4. Resultado

- `patches/c-19-table-figure-layout-cleanup.tex` — diff completo de `introduction.tex` + `results.tex`.
- `PROGRESS.md` fila `C-19` — `applied` (commiteado, pendiente de sync a Overleaf).
- Commit `84a07c4` en `paper-revision`, ya empujado a `origin/main`.

Nada queda pendiente de este bloque — cerrado en su totalidad.
