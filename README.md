# Politicas publicas bajo economia cerrada

Aplicacion Streamlit desarrollada para el Trabajo Practico N.° 2 de Economia para Ingenieros (UNSTA).

## Ejecutar

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Alcance

- Subsidio al transporte publico con analisis de precios, cantidades, excedentes, gasto fiscal y bienestar.
- Precio maximo a los alquileres con escasez, excedentes y perdida de bienestar.
- Simulaciones obligatorias solicitadas en la consigna.
- Interpretacion economica, graficos interactivos y exportacion a Excel.

## Controles interactivos

El panel lateral contiene dos bloques independientes: uno para transporte y otro para alquileres.
Todos los parametros `a`, `b`, `c`, `d` y las dos politicas son editables. Cada cambio recalcula
automaticamente las metricas, formulas visibles, graficos, tablas de simulacion y el archivo Excel.

## Nota metodologica

Para el precio maximo vinculante se supone asignacion eficiente de las unidades disponibles. Esto permite calcular el excedente del consumidor considerando que las viviendas llegan a quienes tienen mayor disposicion a pagar. Un mecanismo de asignacion aleatorio produciria resultados diferentes.
