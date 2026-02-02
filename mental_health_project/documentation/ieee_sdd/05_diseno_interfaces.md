# IEEE 1016 - 05. Diseño de Interfaces (UI/UX)

## 5.1 Arquitectura de la Información (Sitemap)

```mermaid
graph TD
    Home[Inicio / Landing] --> Login[Modal Login]
    Home --> Register[Modal Registro]
    Home --> Authors[Página Autores]
    
    subgraph Protected_Zone [Zona Protegida]
        View_Survey[Formulario Encuesta] --> Results[Resultados IA]
        History[Historial de Evaluaciones]
        Dashboard[Admin: Estadísticas Globales]
        UserMgmt[Admin: Gestión Usuarios]
    end

    Login --> View_Survey
    Login --> Dashboard
```

## 5.2 Diseño de Componentes de Interfaz
- **Navegación Dinámica**: El encabezado cambia según el rol del usuario (Admin vs Usuario Final).
- **Formulario Multietapa con Ayuda Contextual**: Implementación JavaScript para navegación suave entre pasos de la encuesta.
- **Gráficos Estadísticos**: Integración de **Chart.js** para renderizar distribuciones de datos en el Dashboard.

## 5.3 Interfaces Externas
- **Navegadores**: Optimizado para Chrome, Firefox y Safari.
- **Protocolo de Comunicación**: HTTP/HTTPS con respuestas en formato JSON para endpoints de gestión de usuarios (AJAX).
- **Framework de Estilo**: Vanilla CSS con variables CSS personalizadas para mantener una estética consistente (Glassmorphism, Modo Oscuro/Laro equilibrado).

## 5.4 Flujo de Navegación del Usuario (UML Activity)

```mermaid
flowchart TD
    Start([Inicio]) --> Visit[Llega a MindCare]
    Visit --> Auth{¿Está autenticado?}
    Auth -- No --> Guest[Ver Autores o Iniciar Sesión]
    Auth -- Sí --> Role{¿Es Administrador?}
    Role -- Sí --> Admin[Ir a Dashboard Analítico]
    Admin --> Manage[Gestionar Usuarios]
    Role -- No --> Survey[Realizar Encuesta de Salud]
    Survey --> Result[Ver Recomendación IA]
    Guest --> Stop([Fin])
    Manage --> Stop
    Result --> Stop
```

