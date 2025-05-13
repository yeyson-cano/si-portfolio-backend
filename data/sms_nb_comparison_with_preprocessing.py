import pandas as pd
import numpy as np
import zipfile, io, requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
from sklearn.metrics import classification_report, accuracy_score

# 1. Carga del dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip'
resp = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(resp.content))
df = pd.read_csv(
    z.open('SMSSpamCollection'),
    sep='\t', header=None,
    names=['label','message']
)

# Mapear etiquetas
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# 2. Preprocesamiento (minúsculas)
df['message'] = df['message'].str.lower()

# 3. División
X_train, X_test, y_train, y_test = train_test_split(
    df['message'], df['label'],
    test_size=0.2, random_state=42, stratify=df['label']
)

# 4. Vectorización
vect_bern  = CountVectorizer(binary=True)
Xb_train   = vect_bern.fit_transform(X_train)
Xb_test    = vect_bern.transform(X_test)

vect_mul   = CountVectorizer()
Xm_train   = vect_mul.fit_transform(X_train)
Xm_test    = vect_mul.transform(X_test)

vect_tfidf = TfidfVectorizer()
Xt_train   = vect_tfidf.fit_transform(X_train).toarray()
Xt_test    = vect_tfidf.transform(X_test).toarray()

# 5. Entrenamiento
models = {
    "BernoulliNB":  BernoulliNB(),
    "MultinomialNB":MultinomialNB(),
    "GaussianNB":   GaussianNB()
}
X_tr = {"BernoulliNB": Xb_train, "MultinomialNB": Xm_train, "GaussianNB": Xt_train}
X_te = {"BernoulliNB": Xb_test,  "MultinomialNB": Xm_test,  "GaussianNB": Xt_test}

for name, model in models.items():
    model.fit(X_tr[name], y_train)
    y_pred = model.predict(X_te[name])
    print(f"=== {name} ===")
    print(classification_report(y_test, y_pred, target_names=['ham','spam']))
    print("Accuracy:", accuracy_score(y_test, y_pred), "\n")
