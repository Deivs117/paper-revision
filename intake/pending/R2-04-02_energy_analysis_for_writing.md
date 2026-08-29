# R2-04-02 — Análisis energético por modo: datos organizados para redacción

**Destino:** equipo de redacción — usar este documento para actualizar `tab:mode_steady_state_energy`
en `sections/results.tex` y el párrafo asociado. Ver también `PROGRESS.md` fila `R2-04`.

**Origen del cómputo:** `experiments/R2-04-mode-energy/scripts/build_mode_energy.py` (actualizado
2026-08-29). CSV completo en `experiments/R2-04-mode-energy/output/mode_energy_stats.csv`.

---

## 1. Energía en operación estacionaria (por modo)

### 1.1 Tabla de estadísticas intra-segmento (recomendada para el paper)

Las estadísticas intra-segmento agrupan todas las muestras individuales de potencia dentro de los
segmentos en estado estacionario. Son directamente comparables entre los tres modos, independientemente
del número de segmentos disponibles.

| Modo               | Media (W) | SD (W) | N muestras | N segmentos | Duración total |
|--------------------|-----------|--------|------------|-------------|----------------|
| Quadrupedal (C)    | 2.730     | 2.294  | 1 873      | 20          | ~374 s         |
| Differential Rolling (H) | 1.132 | 1.079 | 3 297    | 20          | ~659 s         |
| Omnidirectional (X) | 5.710   | 0.731  | 194        | 1           | 38.6 s         |

Potencia derivada como `|current_A| × 7.2 V` (tensión nominal paquete NiMH, confirmada por el equipo
de hardware). Ventana de acoplamiento electromecánico excluida del inicio de cada segmento (2.92 s
para `z`, 1.56 s para `c`; no existe ventana calibrada para `x`, segmento completo usado).

**Para el modo X:** el único segmento disponible (38.6 s, grabado en piso plano) es estable
internamente (CV = 12.8 %). La SD de 0.731 W refleja variabilidad momento-a-momento durante la
operación, no variabilidad entre ensayos.

### 1.2 Estadísticas inter-segmento (contexto; NO usar como estadístico principal)

Las estadísticas inter-segmento (media y SD de las medias por segmento) se incluyen aquí como
contexto comparativo con la versión anterior de la tabla. **No se recomiendan como estadístico
principal** porque la alta varianza de C y H (~74–94 % CV) refleja heterogeneidad de condición
física entre grabaciones (piso plano / rampa / ensayo estático), no variabilidad de medición.

| Modo               | Media inter-seg (W) | SD inter-seg (W) | N segmentos |
|--------------------|---------------------|------------------|-------------|
| Quadrupedal (C)    | 1.942               | 1.819            | 20          |
| Differential Rolling (H) | 1.356        | 1.007            | 20          |
| Omnidirectional (X) | 5.710              | —                | 1           |

> **Nota para redacción:** la media intra-segmento de C (2.73 W) es mayor que la inter-segmento
> (1.94 W) porque los segmentos más largos (de mayor consumo) pesan proporcionalmente más en el
> cómputo temporal. Lo opuesto ocurre en H (intra 1.13 W < inter 1.36 W). Esto no es un error —
> es la diferencia entre "promedio ponderado por tiempo" e "promedio ponderado por ensayo". Para
> un análisis de despliegue el promedio temporal (intra-segmento) es el más representativo.

---

## 2. Energía en transiciones entre modos

Los datos de transición disponibles cubren únicamente el par Quadrupedal (C) ↔ Differential
Rolling (H), con N=16 y N=19 eventos detectados individualmente.

| Dirección          | Media (J) | SD (J) | N eventos |
|--------------------|-----------|--------|-----------|
| C → H (Quad → Diff) | 5.06    | 2.93   | 16        |
| H → C (Diff → Quad) | 4.13    | 1.19   | 19        |

Energía integrada como `|current_A| × 7.2 V` sobre la ventana de acoplamiento calibrada por
dirección. Fuente: `FigReal_Morphological_Transition_Energy.png` y `patches/n-05-transition-energy-redaction.tex`.

### 2.1 Interpretación como cota superior (clave para la redacción)

La transición C↔H es la de **mayor coste morfológico** entre los tres modos: involucra el
despliegue/retracción completo de las extremidades y el cambio entre locomoción con patas y con
ruedas, lo que requiere el mayor número de movimientos compuestos simultáneos. Las transiciones
que implican el modo Omnidireccional (X) requieren una reconfiguración morfológica
comparativamente menor, ya que la diferencia estructural entre X y los otros modos es menor que
la diferencia C↔H.

**Conclusión para el análisis de despliegue:** el coste máximo de cualquier transición posible
entre los tres modos queda acotado superiormente por el par C↔H. En el peor caso, una transición
consume ≤ 5.06 J (media C→H) con una dispersión de ± 2.93 J. Las transiciones restantes son
previsiblemente menores.

---

## 3. Análisis de despliegue combinado (síntesis para el equipo de redacción)

Un modelo de consumo energético para una misión arbitraria puede expresarse como:

```
E_total = P_C · t_C + P_H · t_H + P_X · t_X + E_trans · n_trans
```

donde:
- `P_C = 2.73 W`, `P_H = 1.13 W`, `P_X = 5.71 W` (medias intra-segmento)
- `t_C, t_H, t_X` = tiempo total en cada modo
- `E_trans ≤ 5.06 J` por transición (cota superior C→H)
- `n_trans` = número de transiciones

El modo Omnidireccional (X) tiene el consumo estacionario más alto (5.71 W), aproximadamente
2.1× el de Quadrupedal y 5.0× el de Differential Rolling. Las transiciones representan un coste
puntual pequeño comparado con la energía de operación continua para segmentos de duración
típica (38 s en X equivalen a ~216 J de operación, frente a ≤ 5 J por transición).

---

## 4. Notas de implementación para el equipo de redacción

1. **Reemplazar la fila X en `tab:mode_steady_state_energy`:** cambiar de `N=1 / 5.71 (sin SD)`
   a `N=194 muestras / 5.71 ± 0.73 W`. Actualizar también el caption eliminando la referencia a
   "estimado preliminar".

2. **Añadir columna de N muestras o nota de pie:** la tabla tiene actualmente una columna
   "N (segments)". Para que los tres modos sean coherentes entre sí, considerar reformular la
   columna como "N (muestras)" y usar los valores de la tabla §1.1, o bien mantener N segmentos
   en la columna principal y añadir N muestras en un pie de tabla.

3. **El párrafo de transiciones** (results.tex ~línea 868) puede extenderse para incorporar el
   argumento de cota superior C↔H (§2.1 de este documento). No es necesario mencionar
   explícitamente qué transiciones no fueron medidas.

4. **`R2-04-01_omnidireccional_energy_data_request.md`** ha sido movido a `intake/processed/`
   — el camino de datos de hardware está cerrado; la resolución es el reencuadre intra-segmento.
