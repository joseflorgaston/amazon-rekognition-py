# Parking Lot AWS Rekognition

Este proyecto es una API desarrollada en Python utilizando Flask que integra AWS Rekognition para detectar vehículos en imágenes de estacionamientos. La API sigue la arquitectura limpia (Clean Architecture) para mantener una estructura modular y fácil de mantener.

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración del Archivo .env](#configuración-del-archivo-env)
- [Inicialización del Proyecto](#inicialización-del-proyecto)
- [Testing](#testing)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas y archivos:

```
parking-lot-aws-rekognition/
├── app/
│   ├── api/                  # Capa de presentación (API de Flask)
│   │   ├── controllers/      # Controladores que manejan las solicitudes HTTP
│   │   │   └── detect_labels_controller.py
│   │   │   └── start_model_controller.py
│   │   │   └── stop_model_controller.py
│   │   │   └── check_model_status_controller.py
│   │   └── routes.py         # Define las rutas de la API
│   │
│   ├── core/                 # Lógica de negocio y casos de uso
│   │   ├── use_cases/        # Casos de uso de la aplicación
│   │   │   └── detect_labels_use_case.py
│   │   │   └── start_model_use_case.py
│   │   │   └── stop_model_use_case.py
│   │   │   └── check_model_status_use_case.py
│   │   └── models/           # Modelos de dominio de negocio
│   │       └── label.py
│   │
│   ├── data/                 # Capa de acceso a datos y servicios externos
│   │   ├── aws_rekognition_service.py  # Servicio que interactúa con AWS Rekognition
│   │   └── repositories/     # Repositorios para interactuar con los datos
│   │       └── label_repository.py
│   │
│   ├── config/               # Configuración del proyecto
│   │   └── config.py         # Configuración y carga de variables de entorno
│   │
│   ├── interfaces/           # Interfaces para los servicios
│   │   └── aws_rekognition_interface.py
│   │
│   └── main.py               # Punto de entrada de la aplicación Flask
│
├── tests/                    # Pruebas unitarias e integración
│   ├── api/
│   ├── core/
│   └── data/
│
├── .env                      # Variables de entorno (no incluido en el repositorio)
├── .gitignore                # Archivos y carpetas a ignorar en Git
├── README.md                 # Documentación del proyecto
└── requirements.txt          # Dependencias del proyecto
```

## Descripcion de carpetas
    app/api: Contiene los controladores y las rutas de la API. Los controladores reciben las solicitudes HTTP y delegan la lógica a los casos de uso correspondientes.
    app/core: Contiene los casos de uso (lógica de negocio) y los modelos de dominio.
    app/data: Lógica de acceso a datos e integración con servicios externos (como AWS Rekognition).
    app/config: Configuraciones del proyecto, incluyendo la carga de variables de entorno.
    app/interfaces: Interfaces para los servicios externos, proporcionando una capa de abstracción para el acceso a AWS Rekognition.
    tests: Pruebas unitarias y de integración.

## Requisitos Previos
    Python 3.8 o superior
    AWS CLI configurado con credenciales válidas
    Credenciales de AWS con permisos para Rekognition (rekognition:StartProjectVersion, rekognition:StopProjectVersion, rekognition:DetectLabels, y rekognition:DescribeProjectVersions) se puede encontrar en la consola de aws/aws-rekognition/custom-labels/Projects/Parking_lot.2024-09-04T18.14.11/Use model

## Instalación
    Clona el repositorio:
git clone https://github.com/tu-usuario/parking-lot-aws-rekognition.git
cd parking-lot-aws-rekognition

    Crea un entorno virtual e instala las dependencias:
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
pip install -r requirements.txt

## Configuración del Archivo .env
Crea un archivo .env en la raíz del proyecto para almacenar las credenciales y configuraciones necesarias. Asegúrate de no incluir este archivo en el control de versiones.

    Ejemplo de archivo .env:
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-2
PROJECT_ARN=arn:aws:rekognition:us-east-2:123456789012:project/tu_proyecto/1234567890123
MODEL_ARN=arn:aws:rekognition:us-east-2:123456789012:project/tu_proyecto/version/tu_modelo/1234567890123
MIN_INFERENCE_UNITS=1
VERSION_NAME=Parking_lot.2024-09-04T18.47.11

## Inicialización del Proyecto
    Para iniciar la API Flask, ejecuta el siguiente comando:
python app/main.py
La API estará disponible en http://127.0.0.1:5000

## Testing
    Para ejecutar las pruebas unitarias, usa:
pytest tests/

## Contribución
Si deseas contribuir a este proyecto, sigue estos pasos:
- Clona el repositorio.
- Crea una rama nueva para tu característica (git checkout -b feature/nueva-caracteristica).
- Realiza un commit de tus cambios (git commit -m 'Añadir nueva característica').
- Realiza un push a la rama (git push origin feature/nueva-caracteristica).
- Abre un Pull Request.