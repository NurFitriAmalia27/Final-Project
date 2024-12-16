import pandas as pd
from sklearn.linear_model import LinearRegression
import pymysql
import pickle

# Fungsi untuk mengambil data dari database
def get_data_from_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysql123',
        database='keuangandb'
    )
    query = "SELECT tanggal, jumlah FROM transaksi"
    df = pd.read_sql(query, connection)
    connection.close()

    # Konversi kolom tanggal menjadi bulan (numerik)
    df['month'] = pd.to_datetime(df['tanggal']).dt.month
    df = df.groupby('month')['jumlah'].sum().reset_index()
    df.rename(columns={'jumlah': 'expenses'}, inplace=True)
    return df

# Fungsi untuk menyimpan model Linear Regression
def save_model():
    df = get_data_from_db()
    print("Data dari database:\n", df)  # Debugging: Menampilkan data

    X = df[['month']]  # Fitur (bulan)
    y = df['expenses']  # Target (pengeluaran)

    # Membuat dan melatih model
    model = LinearRegression()
    model.fit(X, y)

    # Menyimpan model ke file
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print("Model berhasil disimpan sebagai 'model.pkl'.")

if __name__ == '__main__':
    save_model()
