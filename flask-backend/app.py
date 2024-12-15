from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Fungsi untuk memuat model yang telah disimpan
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Endpoint untuk menerima data dan mengembalikan prediksi
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    months = data['months']
    expenses = data['expenses']

    if len(months) != len(expenses):
        return jsonify({'status': 'error', 'message': 'Data tidak valid'})

    # Fitting model
    df = pd.DataFrame({'month': months, 'expenses': expenses})
    X = df[['month']]
    y = df['expenses']
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi pengeluaran bulan depan
    next_month = max(months) + 1
    predicted_expense = model.predict([[next_month]])[0]

    # Membulatkan prediksi ke ratusan terdekat
    rounded_expense = round(predicted_expense, -2)

    # Memformat angka ke bentuk rupiah
    formatted_expense = f"Rp.{rounded_expense:,.0f}".replace(',', '.')

    return jsonify({'status': 'success', 'prediction': formatted_expense})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
