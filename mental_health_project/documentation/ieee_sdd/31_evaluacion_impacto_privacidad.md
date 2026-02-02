# IEEE 1016 - 31. Evaluación de Impacto de Privacidad (DPIA)

## 31.1 Análisis de Flujo de Datos Sensibles
MindCare procesa datos de salud mental, lo que requiere una evaluación rigurosa del impacto en la privacidad de los individuos bajo marcos como el GDPR o leyes locales.

## 31.2 Identificación de Datos de Alto Riesgo
- **Datos Identificables**: Username, Email, IP (registrada en logs de servidor).
- **Datos Sensibles**: Respuestas sobre historial familiar, interferencia laboral y consecuencias de salud mental.

## 31.3 Evaluación de Riesgos de Privacidad

| Actividad de Procesamiento | Riesgo Identificado | Nivel de Riesgo | Medida de Mitigación |
| :--- | :--- | :--- | :--- |
| **Inferencia de IA** | Re-identificación a través de patrones de respuesta. | Medio | Agregación de datos y anonimización de reportes administrativos. |
| **Almacenamiento** | Acceso no autorizado a la base de datos SQLite. | Alto | Cifrado a nivel de sistema de archivos y permisos restrictivos (600). |
| **Visualización Admin** | Exposición de respuestas individuales a superusuarios. | Medio | Implementación de vistas de "solo resumen" (Aggregate Views). |

## 31.4 Ciclo de Vida de la Privacidad

```mermaid
graph LR
    Collect[Recolección con Consentimiento] --> Process[Procesamiento Mínimo]
    Process --> Storage[Almacenamiento Cifrado]
    Storage --> Deletion[Derecho al Olvido / Borrado]
```

## 31.5 Declaración de Conformidad
El sistema se diseña para cumplir con el principio de "Privacidad desde el Diseño", asegurando que la protección de datos sea una característica intrínseca del software y no un parche posterior.
