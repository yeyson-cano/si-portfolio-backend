# SI Portfolio Backend

API REST en **FastAPI** para el portafolio de mini-proyectos de Software Inteligente.  
Todo el entorno de ejecución (Conda, dependencias y base de datos) se orquesta con **Docker Compose**.

---

## 🔍 Descripción

Este servicio ofrece:

- Metadatos de proyectos (Genético, Naive Bayes, Red Neuronal, Visión por Computadora)  
- Archivos asociados (scripts, datos, notebooks, videos)  
- Ejecución dinámica de cada algoritmo con parámetros a medida o entrada por imagen  

---

## 🤖 Algoritmos soportados

1. **Algoritmo Genético (GA)**  
   - Optimización de rutas para vehículos (VRP)  
   - Parámetros: tamaño de población, generaciones, tasa de mutación, elitismo, etc.  
   - Salida: evolución de fitness, estado de la primera generación y solución óptima.

2. **Naive Bayes (NB)**  
   - Clasificación de SMS en ham/spam usando Bernoulli, Multinomial y Gaussian NB  
   - Parámetros: proporción de test, vectorización (binary/count/TF-IDF), limpieza de texto.  
   - Salida: métricas (accuracy, precision, recall, F1), matriz de confusión y muestras de predicción.

3. **Red Neuronal Manual (NN)**  
   - Red feed-forward con 2 neuronas de entrada, 2 ocultas, 1 de salida  
   - Parámetros: pesos iniciales (entrada→oculta y oculta→salida), dataset, tasa de aprendizaje.  
   - Salida: detalle de forward/backprop para cada muestra y pesos finales.

4. **Visión por Computadora (CNN)**  
   - Clasificación de flores (daisy, dandelion, roses, sunflowers, tulips)  
   - Entrada: imagen JPG o PNG subida por el usuario  
   - Salida: clase predicha y nivel de confianza

5. **Reconocimiento de Entidades Nombradas (NER)** ✅  
   - Modelo BERT preentrenado para extraer entidades tipo persona (PER), organización (ORG), ubicación (LOC), etc.  
   - Entrada: texto plano  
   - Salida: lista de entidades reconocidas con su tipo y nivel de confianza  
   - **Ejemplo CURL con autenticación básica:**  
     ```bash
     curl -X POST http://TU_IP_PUBLICA:8000/execute/ner \
     -u admin:admin123 \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Pedro Sánchez es el presidente del Gobierno de España."
     ```

---

## 🚀 Tecnologías

- **FastAPI** + **Uvicorn**  
- **PostgreSQL 15**  
- **SQLAlchemy (asyncio)** + **asyncpg**  
- **TensorFlow** + **Pillow** para procesamiento de imágenes  
- **Transformers (HuggingFace)** para NER  
- **Conda** (Miniforge) dentro de Docker  
- **Docker & Docker Compose**  
- **scikit-learn**, **pandas**, **numpy**, **requests**, **python-multipart**

---

## 📦 Puesta en marcha

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/yeyson-cano/si-portfolio-backend.git
   cd si-portfolio-backend
   ```

2. **Instala Docker y Docker Compose**

3. **Levanta los servicios**

   ```bash
   docker-compose up --build -d
   ```

4. **Inicializa la base de datos**

   ```bash
   docker-compose exec backend \
   bash -c "conda run -n si-backend python -m app.models.init_db"
   ```

5. **Verifica**

   * API: [http://localhost:8000/](http://localhost:8000/)
   * Swagger / OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗂 Estructura del proyecto

```
.
├── Makefile            # Tareas de inicialización y migración de BD
├── app/
│   ├── algorithms/     # Lógica de ejecución de cada algoritmo
│   ├── db.py           # Configuración de SQLAlchemy
│   ├── main.py         # Punto de entrada FastAPI
│   ├── models/         # Modelos SQLAlchemy
│   ├── repository.py   # Capa de acceso a datos y ejecución
│   ├── routes/         # Routers de FastAPI
│   └── schemas/        # Esquemas Pydantic
├── data/               # Datos estáticos (p.ej. SMSSpamCollection.csv)
├── saved_models/       # Modelos entrenados (e.g. CNN de flores)
├── environment.yml     # Definición de entorno Conda
├── Dockerfile          # Imagen con Conda y Uvicorn
├── docker-compose.yml  # Orquesta servicios: postgres + backend
└── README.md
```

---

## 🔌 Endpoints principales

* **GET** `/projects`
* **GET** `/projects/{project_id}`
* **GET** `/files/projects/{project_id}/files`
* **GET** `/files/{file_id}`

### 📥 POST `/execute/{algorithm_key}`

Para algoritmos tradicionales (genetic, nb, nn):

```json
{
  "params": { /* según algoritmo */ },
  "verbosity": "first" | "all" | "final"
}
```