import pandas as pd
from sklearn.linear_model import LinearRegression
import pymysql
import pickle

# Fungsi untuk mengambil data transaksi dan income dari database
def get_data_from_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysql123',
        database='keuangandb'
    )
    query_transaksi = "SELECT tanggal, jumlah, kategori FROM transaksi"
    query_income = "SELECT month, amount FROM income"

    df_transaksi = pd.read_sql(query_transaksi, connection)
    df_income = pd.read_sql(query_income, connection)
    connection.close()

    df_transaksi['month'] = pd.to_datetime(df_transaksi['tanggal']).dt.month
    df_transaksi_monthly = df_transaksi.groupby(['month', 'kategori'])['jumlah'].sum().reset_index()

    df = pd.merge(df_transaksi_monthly, df_income, on='month', how='left')
    df['expenses'] = df['jumlah']
    df['income'] = df['amount']

    return df

# Fungsi untuk melatih model
def save_model():
    df = get_data_from_db()
    X = pd.get_dummies(df[['month', 'kategori', 'income']], drop_first=True)
    y = df['expenses']

    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)

    model = LinearRegression()
    model.fit(X, y)

    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print("Model berhasil diperbarui dan disimpan.")
