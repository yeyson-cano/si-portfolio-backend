# app/algorithms/nb.py

import os
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Ruta al CSV local (versión descomprimida de SMSSpamCollection)
DATA_PATH = os.getenv("NB_DATA_PATH", "data/SMSSpamCollection.csv")

def _load_dataset() -> pd.DataFrame:
    """
    Carga y prepara el dataset de SMS desde el archivo CSV en DATA_PATH.
    Se espera que tenga encabezados: v1 (label), v2 (message)
    """
    df = pd.read_csv(
        DATA_PATH,
        encoding="latin1",
        encoding_errors="replace"
    )
    df = df[['v1', 'v2']]  # Tomar solo las columnas relevantes
    df.columns = ['label', 'message']  # Renombrarlas

    # Mapear etiquetas a 0 y 1
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})

    return df

def _compute_metrics(y_true, y_pred) -> Dict[str, float]:
    """Devuelve un diccionario con accuracy, precision, recall y f1."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0)
    }

def run_naive_bayes(params: Dict[str, Any], verbosity: str) -> Dict[str, Any]:
    """
    :param params: {
        "test_size": float (entre 0 y 1),
        "random_state": int,
        # opcionalmente flags de limpieza: "lowercase": bool, ...
    }
    :param verbosity: "first"|"all"|"final"
    :returns: {
      "metrics": {
        "BernoulliNB": {...},
        "MultinomialNB": {...},
        "GaussianNB": {...}
      },
      # opcionalmente "confusion": {
      #    "BernoulliNB": [[TN, FP],[FN, TP]], …
      # }
      # opcionalmente "samples": [ { "message":..., "true":0, "pred":1 }, … ] 
    }
    """
    # 1. Carga y limpieza
    df = _load_dataset()
    if params.get("lowercase", True):
        df['message'] = df['message'].str.lower()
    # … aquí podrías añadir más preprocessing según params …

    # 2. División
    test_size = params.get("test_size", 0.2)
    random_state = params.get("random_state", 42)
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label'],
        test_size=test_size,
        random_state=random_state,
        stratify=df['label']
    )

    # 3. Vectorización
    vect_bern = CountVectorizer(binary=True)
    Xb_train = vect_bern.fit_transform(X_train)
    Xb_test  = vect_bern.transform(X_test)

    vect_mul = CountVectorizer()
    Xm_train = vect_mul.fit_transform(X_train)
    Xm_test  = vect_mul.transform(X_test)

    vect_tfidf = TfidfVectorizer()
    Xt_train = vect_tfidf.fit_transform(X_train).toarray()
    Xt_test  = vect_tfidf.transform(X_test).toarray()

    # 4. Entrenamiento
    models = {
        "BernoulliNB": BernoulliNB(),
        "MultinomialNB": MultinomialNB(),
        "GaussianNB": GaussianNB()
    }
    data_train = {
        "BernoulliNB": (Xb_train, y_train),
        "MultinomialNB": (Xm_train, y_train),
        "GaussianNB": (Xt_train, y_train)
    }
    data_test = {
        "BernoulliNB": (Xb_test, y_test),
        "MultinomialNB": (Xm_test, y_test),
        "GaussianNB": (Xt_test, y_test)
    }

    metrics = {}
    confusion = {}
    samples = []

    for name, model in models.items():
        Xtr, ytr = data_train[name]
        Xte, yte = data_test[name]
        model.fit(Xtr, ytr)
        y_pred = model.predict(Xte)

        metrics[name] = _compute_metrics(yte, y_pred)
        confusion[name] = confusion_matrix(yte, y_pred).tolist()

        # Si piden al menos algo de sample output
        if verbosity in ("first", "all"):
            # Tomamos las primeras 5 pruebas
            for msg, true, pred in zip(X_test[:5], yte[:5], y_pred[:5]):
                samples.append({
                    "message": msg if isinstance(msg, str) else "",
                    "true": int(true),
                    "pred": int(pred),
                    "model": name
                })

    result: Dict[str, Any] = {
        "metrics": metrics
    }
    if verbosity in ("first", "all"):
        result["confusion"] = confusion
        result["samples"] = samples
    return {
        "history": [],          # NB no usa history de generaciones
        "first_epoch": None,    # NB no tiene primera iteración análoga
        "final": result
    }
