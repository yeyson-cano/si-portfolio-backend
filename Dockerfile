# 1. Imagen base con Miniforge (Conda ligero)
FROM condaforge/miniforge3

# 2. Directorio de trabajo
WORKDIR /app

# 3. Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    DATABASE_URL=postgresql+asyncpg://si_user:si_password_segura@db/si_portfolio

# 4. Copiar el environment.yml y crear el entorno
COPY environment.yml .
RUN conda env create -f environment.yml && \
    conda clean --all --yes

# 5. Copiar el resto del código al contenedor
COPY . .

# 6. Descargar el modelo NER en la etapa de construcción
RUN conda run -n si-backend python app/scripts/download_ner_model.py

# 7. Exponer el puerto de la API
EXPOSE 8000

# 8. ENTRYPOINT para ejecutar todo dentro del entorno Conda 'si-backend'
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "si-backend", "python", "-m"]

# 9. CMD por defecto: arranca Uvicorn en modo reload para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
