from flask import Flask, request, jsonify
import pickle
import pandas as pd
from model import save_model, get_data_from_db

app = Flask(__name__)

# Memuat model yang telah disimpan
def load_model():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data['model'], data['std_dev']

# Endpoint untuk pelatihan ulang model
@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        save_model()  
        global model, std_dev
        model, std_dev = load_model()  
        return jsonify({'status': 'success', 'message': 'Model berhasil dilatih ulang.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Load model saat aplikasi dimulai
model, std_dev = load_model()

# Endpoint untuk prediksi pengeluaran bulan depan
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        months = data.get('months', [])

        if not months:
            return jsonify({'status': 'error', 'message': 'Data bulan tidak ditemukan.'}), 400

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
        formatted_std_dev = f"Rp.{std_dev:,.0f}".replace(',', '.')
        return jsonify({
            'status': 'success',
            'prediction': formatted_expense,
            'std_dev': formatted_std_dev
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Endpoint untuk chart data
@app.route('/transaksi/chart-data')
def chart_data():
    try:
        df = get_data_from_db()

        # Data untuk Pie Chart
        category_data = df.groupby('kategori')['jumlah'].sum()
        categories = category_data.index.tolist()
        amounts = category_data.values.tolist()

        # Data untuk Bar Chart
        monthly_data = df.groupby('month')['jumlah'].sum()
        months = monthly_data.index.tolist()
        monthly_amounts = monthly_data.values.tolist()

        months_sorted = sorted(months)
        monthly_amounts_sorted = [monthly_amounts[months.index(month)] for month in months_sorted]

        return jsonify({
            'categories': categories,
            'amounts': amounts,
            'months': months_sorted,
            'monthly_amounts': monthly_amounts_sorted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
