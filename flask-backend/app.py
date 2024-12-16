from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Fungsi untuk memuat model yang telah disimpan
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Load model saat aplikasi dimulai
model = load_model()

# Endpoint untuk prediksi pengeluaran bulan depan
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        months = data.get('months', [])

        if not months:
            return jsonify({'status': 'error', 'message': 'Data bulan tidak ditemukan.'}), 400

        # Prediksi pengeluaran bulan depan
        next_month = max(months) + 1
        predicted_expense = model.predict([[next_month]])[0]

        # Membulatkan prediksi ke ratusan terdekat
        rounded_expense = round(predicted_expense, -2)
        formatted_expense = f"Rp.{rounded_expense:,.0f}".replace(',', '.')

        return jsonify({'status': 'success', 'prediction': formatted_expense})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
