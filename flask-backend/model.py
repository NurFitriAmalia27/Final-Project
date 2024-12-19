import pandas as pd
from sklearn.linear_model import LinearRegression
import pymysql
import pickle
import numpy as np

# Mengambil data transaksi dari database
def get_data_from_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysql123',
        database='keuangandb'
    )
    query_transaksi = "SELECT tanggal, jumlah, kategori FROM transaksi"
    df_transaksi = pd.read_sql(query_transaksi, connection)
    connection.close()

    # Konversi kolom tanggal menjadi bulan
    df_transaksi['month'] = pd.to_datetime(df_transaksi['tanggal']).dt.month
    return df_transaksi

# Melatih model
def save_model():
    df = get_data_from_db()

    # Kelompokkan data per bulan dan kategori
    df_monthly = df.groupby(['month', 'kategori'])['jumlah'].sum().reset_index()

    # Debugging
    print("Data setelah pengelompokkan per bulan dan kategori:")
    print(df_monthly)

    # Kelompokkan data hanya berdasarkan bulan untuk menghindari duplikat
    df_monthly_total = df_monthly.groupby('month')['jumlah'].sum().reset_index()

    # Pastikan semua bulan (1–12) ada, meskipun kosong
    full_months = pd.DataFrame({'month': range(1, 13)})
    df_monthly_total = pd.merge(full_months, df_monthly_total, on='month', how='left').fillna(0)

    # Debugging
    print("Total pengeluaran per bulan (termasuk bulan kosong):")
    print(df_monthly_total)

    # One-hot encoding untuk kategori (gunakan df_monthly asli)
    X = pd.get_dummies(df_monthly[['month', 'kategori']], drop_first=True)
    y = df_monthly_total['jumlah']  # Gunakan total jumlah bulanan

    # Pastikan tidak ada nilai NaN
    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)

    # Debugging
    print(f"Shape of X: {X.shape}")
    print(f"Shape of y: {y.shape}")
    print("Fitur (X):")
    print(X.head())
    print("Target (y):")
    print(y.head())

    # Perbaikan jika panjang X dan y tidak sesuai
    if len(X) != len(y):
        print("Panjang X dan y tidak sesuai. Menyesuaikan...")
        X = X.iloc[:len(y)]

    # Latih model regresi linear
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi untuk data pelatihan
    y_pred = model.predict(X)

    # Hitung standar deviasi residual
    residuals = y - y_pred
    std_dev = np.std(residuals)

    # Simpan model dan standar deviasi ke file
    with open('model.pkl', 'wb') as file:
        pickle.dump({'model': model, 'std_dev': std_dev}, file)
    print("Model dan standar deviasi berhasil diperbarui dan disimpan.")

if __name__ == '__main__':
    save_model()
