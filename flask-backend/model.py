import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pymysql
import pickle
from sklearn.metrics import mean_squared_error, r2_score

# Fungsi untuk mengambil data dari database
def get_data_from_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysql123',  
        database='keuangandb'
    )
    
    query = "SELECT month, expenses FROM transactions"
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df

# Fungsi untuk melatih model Linear Regression dan memprediksi pengeluaran bulan depan
def predict_expenses(month):
    df = get_data_from_db()
    
    # Membuat model Linear Regression
    X = df[['month']]  # Fitur (bulan)
    y = df['expenses']  # Target (pengeluaran)

    # Split data menjadi training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluasi model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")
    
    # Prediksi pengeluaran bulan depan
    predicted_expenses = model.predict([[month + 1]])  
    
    return predicted_expenses[0]

# Fungsi untuk menyimpan model yang sudah dilatih
def save_model():
    df = get_data_from_db()
    model = LinearRegression()
    model.fit(df[['month']], df['expenses'])
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
