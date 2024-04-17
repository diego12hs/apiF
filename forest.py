from flask import Flask, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from flask import Flask, send_from_directory
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory('static', 'script.js')
@app.route('/train_model', methods=['GET'])
def train_model():
    try:
        # Paso 1: Leer los primeros 20 registros del archivo CSV
        datos = pd.read_csv('TotalFeatures-ISCXFlowMeter.csv')

        # Paso 2: Separar características (features) y etiquetas (labels)
        if 'calss' in datos.columns:
            X = datos.drop('calss', axis=1)  # Características
            y = datos['calss']  # Etiquetas
        else:
            return jsonify({"error": "Columna 'class' no encontrada en los datos"})

        # Paso 3: Convertir características no numéricas usando codificación one-hot
        X = pd.get_dummies(X)

        # Paso 4: Dividir datos en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Paso 5: Crear un clasificador RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)

        # Paso 6: Entrenar el modelo
        clf.fit(X_train, y_train)

        # Paso 7: Evaluar el modelo
        y_pred = clf.predict(X_test)
        classification_rep = classification_report(y_test, y_pred)

        # Paso 8: Calcular el porcentaje de precisión
        accuracy = accuracy_score(y_test, y_pred)

        # Paso 9: Obtener la predicción del modelo para un ejemplo de prueba
        example_prediction = clf.predict(X_test.iloc[[0]])[0]

        # Devolver el informe de clasificación, la precisión y la predicción como respuesta
        return jsonify({"classification_report": classification_rep, "accuracy": accuracy, "example_prediction": example_prediction})

    except Exception as e:
        return jsonify({"error": f"Se produjo un error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
