import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'C:/Users/Nur Fitri Amalia/Latihan Minggu 11/backend/instance/model_regression.pkl')

def load_model():
    try:
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
        print("Model berhasil dimuat.")
        return model
    except Exception as e:
        print(f"Error saat memuat model: {e}")
        raise e
