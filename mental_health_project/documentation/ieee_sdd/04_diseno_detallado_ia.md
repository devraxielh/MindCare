# IEEE 1016 - 04. Diseño de Detalle (Inteligencia Artificial)

## 4.1 Especificación del Modelo
El "cerebro" de MindCare es un clasificador basado en el algoritmo **Random Forest**, entrenado con el dataset de salud mental en la industria tech.

## 4.2 Pipeline de Inferencia (Diagrama de Estado UML)
El proceso desde que se recibe la encuesta hasta que se entrega la predicción.

```mermaid
stateDiagram-v2
    [*] --> Recepcion: Usuario envía POST
    Recepcion --> Preprocesamiento: Conversión de texto a numérico
    Preprocesamiento --> Inferencia: Carga de modelo (.joblib)
    Inferencia --> Generacion_Etiqueta: Aplicar predicción
    Generacion_Etiqueta --> Almacenamiento: Guardar en DB
    Almacenamiento --> Despliegue: Mostrar en Results.html
    Despliegue --> [*]
```

## 4.3 Diagrama de Secuencia de Predicción (UML Sequence)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant V as View (survey)
    participant M as ML Utils (inference)
    participant DB as SQLite DB

    U->>V: Envía respuestas formulario
    V->>V: Valida integridad de datos (Forms)
    V->>M: Enviar datos para predicción
    M->>M: Codificar variables (One-Hot)
    M->>M: Ejecutar Clasificación (RF)
    M-->>V: Retorna Recomendación (Tratamiento/No)
    V->>DB: Almacena respuesta y predicción
    V-->>U: Redirige a página de resultados
```

## 4.4 Características del Modelo
- **Variables de entrada**: 16 variables categóricas y numéricas.
- **Tipo de aprendizaje**: Supervisado (Clasificación binaria).
- **Herramientas**: Scikit-Learn, Joblib, NumPy, Pandas.
- **Interpretabilidad**: El uso de Random Forest permite extraer la importancia de las características (Feature Importance), lo cual es crucial para la ética en salud mental.
