# Exploración

> **Trabajo extra, por curiosidad.** Todo lo que hay en esta carpeta (notebooks, scripts, resultados y observaciones) surgió de seguir jugando con los datos después de terminar el proyecto, para responder preguntas que nos fueron apareciendo. No forma parte de la entrega principal ni es necesario para evaluarla, y ninguna de sus conclusiones modifica los resultados de las notebooks 01 a 07.
>
> Por ser exploratorio, el nivel de validación es menor que el del proyecto: algunas decisiones se tomaron mirando los mismos meses con los que después se evaluaron, y los resultados deben leerse como pistas para seguir investigando, no como pronósticos oficiales.

Las preguntas que nos hicimos fueron tres:

1. El pronóstico de agosto no incluye los pozos que se conectan durante el mes. ¿Cuánto cambia el total si los sumamos?
2. El pronóstico es un único número. ¿Entre qué valores puede quedar realmente la producción?
3. Un mes de anticipación es poco para planificar. ¿Qué pasa si pronosticamos a 3 y 6 meses?

Los análisis parten de los archivos que generan las notebooks 01 a 03 en `data/processed` y usan la misma configuración de Random Forest que la notebook 04, entrenada con los últimos 24 meses.

| Notebook | Pregunta |
|---|---|
| `01_pozos_nuevos.ipynb` | ¿Cuánto aportan los pozos que se conectan después del mes de corte y cómo se pronostica ese aporte? |
| `02_rango_del_pronostico.ipynb` | ¿Entre qué valores puede quedar la producción total? Incluye un pronóstico rodante de 19 meses y una regresión por cuantiles por pozo. |
| `03_pronostico_3_y_6_meses.ipynb` | ¿Qué producción esperamos en octubre de 2026 y enero de 2027? |

Las funciones compartidas están en `comun.py` y los resultados se guardan en `resultados/`.

## Cómo ejecutarlas

Primero hay que ejecutar las notebooks 01 a 04 del proyecto. Después, desde esta carpeta, se ejecutan en orden:

```bash
jupyter nbconvert --to notebook --execute --inplace 01_pozos_nuevos.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_rango_del_pronostico.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_pronostico_3_y_6_meses.ipynb
```

Los pronósticos rodantes entrenan 39 modelos, lo que lleva alrededor de una hora. Sus resultados se guardan en `resultados/cache/`; si esos archivos existen, se reutilizan. Para recalcularlos hay que borrar la carpeta.

## Resultados principales

| | Agosto 2026 | Octubre 2026 | Enero 2027 |
|---|---|---|---|
| Pozos que producían en julio | 3,24 M m³ (+1,2 %) | 3,10 M m³ (−2,9 %) | 2,69 M m³ (−15,9 %) |
| Pozos conectados después de julio | 0,03 M m³ | 0,43 M m³ | 1,10 M m³ |
| **Total** | **3,27 M m³ (+2,2 %)** | **3,53 M m³ (+10,4 %)** | **3,79 M m³ (+18,5 %)** |
| Rango del 80 % | 3,10 a 3,38 M m³ | 3,47 a 3,77 M m³ | 3,71 a 4,07 M m³ |
| Error medio del total en el pronóstico rodante | 3,0 % | 3,4 % | 4,8 % |
| Error medio de la persistencia | 5,1 % | 6,2 % | 11,8 % |

Los porcentajes son respecto de julio de 2026 (3,20 M m³).

- Los pozos nuevos pesan menos del 1 % del total del mes en que se conectan, el 11 % a 3 meses y el 28 % a 6 meses.
- Cada camada de pozos nuevos produce entre 20 % y 30 % más que la del año anterior. El pronóstico de su aporte lo tiene en cuenta.
- El modelo no ajusta por la cantidad de días del mes: febrero y marzo concentran los errores más grandes.
- Los pronósticos a 3 y 6 meses suponen que se mantiene el ritmo de unos 49 pozos nuevos por mes.
