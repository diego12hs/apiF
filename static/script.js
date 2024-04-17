document.getElementById('trainButton').addEventListener('click', function() {
    fetch('/train_model')
    .then(response => response.json())
    .then(data => {
        document.getElementById('classificationReport').innerText = "Informe de Clasificación:\n" + data.classification_report;
        document.getElementById('accuracy').innerText = "Precisión del Modelo:\n " + (data.accuracy * 100).toFixed(2) + "%";
        document.getElementById('examplePrediction').innerText = "Predicción:\n " + data.example_prediction;
        document.getElementById('resultContainer').style.display = 'block';
    })
    .catch(error => console.error('Error al obtener los datos:', error));
});
