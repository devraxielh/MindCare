# IEEE 1016 - 02. Arquitectura del Sistema

## 2.1 Patrón Arquitectónico: MVT (Model-View-Template)
MindCare implementa el patrón MVT de Django para desacoplar la gestión de datos, la lógica de control y la interfaz de usuario.

### 2.2 Diagrama de Arquitectura Detallado (UML Package)

```mermaid
graph TB
    subgraph Frontend_Layer [Capa de Presentación]
        HTML[Templates HTML5]
        CSS[Vanilla CSS / Estilos]
        JS[JavaScript / Chart.js]
    end

    subgraph Logic_Layer [Capa de Lógica de Negocio]
        URLs[URL Dispatcher]
        Views[Views / Lógica]
        Forms[Forms / Validación]
        Auth[Sistema de Autenticación]
    end

    subgraph AI_Engine [Capa de Inteligencia Artificial]
        ML_Utils[Wrapper Inferencia]
        ML_Model[Joblib / Random Forest]
    end

    subgraph Data_Layer [Capa de Datos]
        ORM[Django ORM]
        DB[(SQLite 3 Database)]
    end

    Frontend_Layer <--> URLs
    URLs <--> Views
    Views <--> Forms
    Views <--> Templates
    Views <--> Auth
    Views <--> ML_Utils
    ML_Utils <--> ML_Model
    Views <--> ORM
    ORM <--> DB
```

## 2.3 Descomposición de Subsistemas
1.  **Subsistema de Encuestas**: Gestiona la lógica multietapa de la captura de datos.
2.  **Subsistema de Identidad**: Basado en `django.contrib.auth`, maneja el control de acceso basado en roles (RBAC).
3.  **Subsistema Analítico**: Procesa las respuestas almacenadas para generar distribuciones estadísticas a través de `Chart.js`.
4.  **Subsistema Predictivo**: Componente asíncrono que realiza inferencias ML.

## 2.4 Decisiones Técnicas Clave
- **Django**: Elegido por su seguridad integrada (Batteries included).
- **SQLite**: Utilizado por su portabilidad para entornos de investigación.
- **Random Forest**: Seleccionado por su capacidad para manejar datos categóricos y su interpretabilidad.
