# IEEE 1016 - 17. Ética de Ingeniería y Privacidad de la IA

## 17.1 Principios Éticos de MindCare
Dado que el sistema maneja información de salud mental, la ética no es un añadido, sino una base de la ingeniería del software.

1.  **Beneficencia**: El sistema debe priorizar el bienestar del usuario sobre cualquier métrica comercial.
2.  **No maleficencia**: Los algoritmos no deben usarse para discriminar a empleados por su estado mental.
3.  **Transparencia**: El usuario debe saber que interactúa con una IA y cómo se procesan sus datos.

## 17.2 Privacidad por Diseño (Privacy by Design)
- **Anonimización**: Los resultados estadísticos en el dashboard no revelan la identidad del usuario a los administradores.
- **Minimización de Datos**: Solo se solicitan los datos estrictamente necesarios para el funcionamiento del modelo de IA.
- **Cifrado de Extremo a Extremo**: Los datos sensibles viajan bajo protocolos seguros (HTTPS) y se almacenan con hashing.

## 17.3 Diagrama de Ciclo de Datos Ético

```mermaid
graph LR
    Input[Entrada de Datos] --> Encrypt[Cifrado]
    Encrypt --> Predict[Inferencia IA]
    Predict --> Output[Resultado Personalizado]
    Output --> Stats[Estadísticas Agregadas Anónimas]
    Stats --> Admin[Dashboard]
```

## 17.4 Responsabilidad Algorítmica
MindCare incluye una cláusula de responsabilidad que aclara que el modelo es una **herramienta de tamizaje**, no un juicio clínico definitivo.
