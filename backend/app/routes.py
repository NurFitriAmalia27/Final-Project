from flask import Blueprint, jsonify, request, send_file
from flask_cors import CORS
from .services.prediction_service import predict_expense
import matplotlib.pyplot as plt
import os

main = Blueprint('main', __name__)
CORS(main)

# Rute prediksi
@main.route('/predict', methods=['POST'])
def predict():
    try:
        if not request.is_json:
            return jsonify({"status": "error", "message": "Request must be JSON"}), 400

        data = request.json
        month = data.get('month')
        if month is None or not (1 <= month <= 12):
            return jsonify({"status": "error", "message": "Invalid month value. Must be between 1 and 12."}), 400

        prediction = predict_expense(month)
        return jsonify({"status": "success", "prediction": prediction})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Rute untuk grafik pengeluaran
@main.route('/chart', methods=['GET'])
def generate_pie_chart():
    transactions = Transaksi.query.all()  # Semua transaksi dianggap pengeluaran
    category_totals = {}
    for t in transactions:
        category_totals[t.kategori] = category_totals.get(t.kategori, 0) + t.jumlah

    labels = list(category_totals.keys())
    values = list(category_totals.values())
    fig = Figure()
    ax = fig.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Pengeluaran per Kategori")

    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

