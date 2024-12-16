import matplotlib.pyplot as plt
import os
import pymysql
import pandas as pd

# Fungsi untuk mengambil data dari database
def get_data_from_db():
    try:
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

        # Konversi kolom tanggal menjadi bulan
        df_transaksi['month'] = pd.to_datetime(df_transaksi['tanggal']).dt.month
        df_transaksi_monthly = df_transaksi.groupby(['month', 'kategori'])['jumlah'].sum().reset_index()

        return df_transaksi_monthly
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

# Fungsi untuk memastikan folder tersedia
def ensure_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Fungsi untuk menghasilkan grafik
def generate_charts():
    df = get_data_from_db()

    # Folder untuk menyimpan chart
    chart_folder = os.path.join('static', 'charts')
    ensure_folder(chart_folder)

    # Pie chart berdasarkan total pengeluaran per kategori
    category_data = df.groupby('kategori')['jumlah'].sum()
    categories = category_data.index.tolist()
    amounts = category_data.values.tolist()
    percentages = [amount / sum(amounts) * 100 for amount in amounts]

    fig1, ax1 = plt.subplots()
    ax1.pie(amounts, labels=[f'{cat} ({percent:.1f}%)' for cat, percent in zip(categories, percentages)], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    fig1.savefig(os.path.join(chart_folder, 'pie_chart.png'))

    # Bar chart pengeluaran bulanan
    monthly_data = df.groupby('month')['jumlah'].sum()
    months = monthly_data.index.tolist()
    amounts = monthly_data.values.tolist()

    fig2, ax2 = plt.subplots()
    ax2.bar(months, amounts)
    ax2.set_xlabel('Bulan')
    ax2.set_ylabel('Pengeluaran (Rp)')
    ax2.set_title('Pengeluaran Per Bulan')
    fig2.savefig(os.path.join(chart_folder, 'bar_chart.png'))

    plt.close(fig1)
    plt.close(fig2)
    print("Grafik berhasil disimpan di folder static/charts.")

if __name__ == '__main__':
    generate_charts()
