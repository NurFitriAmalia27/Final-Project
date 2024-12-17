from flask import Flask, request, jsonify
import pickle
import pandas as pd
from model import save_model  

app = Flask(__name__)

# Fungsi untuk memuat model yang telah disimpan
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Endpoint untuk pelatihan ulang model
@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        save_model()  
        global model
        model = load_model()  
        return jsonify({'status': 'success', 'message': 'Model berhasil dilatih ulang.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Load model saat aplikasi dimulai
model = load_model()

# Endpoint untuk prediksi pengeluaran bulan depan
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data dari request
        data = request.get_json()
        months = data.get('months', [])

        if not months:
            return jsonify({'status': 'error', 'message': 'Data bulan tidak ditemukan.'}), 400

        # Data prediksi hanya menggunakan bulan tanpa income
        next_month = max(months) + 1
        input_data = pd.DataFrame({'month': [next_month], 'kategori': ['dummy']})
        input_data = pd.get_dummies(input_data, drop_first=True)

        model_features = model.feature_names_in_
        for col in model_features:
            if col not in input_data.columns:
                input_data[col] = 0

        input_data = input_data[model_features]
        predicted_expense = model.predict(input_data)[0]
        rounded_expense = round(predicted_expense, -2)
        formatted_expense = f"Rp.{rounded_expense:,.0f}".replace(',', '.')

        return jsonify({'status': 'success', 'prediction': formatted_expense})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

