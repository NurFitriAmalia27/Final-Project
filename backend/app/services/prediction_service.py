from ..models.regression_model import load_model

def predict_expense(month):
    try:
        model = load_model()  # Memuat model
        prediction = model.predict([[month]])[0]  # Prediksi untuk bulan yang diterima
        return prediction
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None
