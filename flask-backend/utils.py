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
        df_transaksi = pd.read_sql(query_transaksi, connection)
        connection.close()

        # Konversi kolom tanggal menjadi bulan
        df_transaksi['month'] = pd.to_datetime(df_transaksi['tanggal']).dt.month
        return df_transaksi
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

# Fungsi untuk memastikan folder tersedia
def ensure_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Fungsi untuk menghasilkan grafik
def generate_charts():
    # Ambil data dari database
    df = get_data_from_db()

    # Pastikan folder untuk menyimpan chart tersedia
    chart_folder = os.path.join('static', 'charts')
    ensure_folder(chart_folder)  # Pastikan folder tersedia

    # Pie chart berdasarkan total pengeluaran per kategori
    try:
        category_data = df.groupby('kategori')['jumlah'].sum()
        categories = category_data.index.tolist()
        amounts = category_data.values.tolist()
        percentages = [amount / sum(amounts) * 100 for amount in amounts]

        fig1, ax1 = plt.subplots()
        ax1.pie(amounts, labels=[f'{cat} ({percent:.1f}%)' for cat, percent in zip(categories, percentages)],
                autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        fig1.savefig(os.path.join(chart_folder, 'pie_chart.png'))
        plt.close(fig1)
    except Exception as e:
        print(f"Error generating pie chart: {e}")

    # Bar chart pengeluaran bulanan
    try:
        monthly_data = df.groupby('month')['jumlah'].sum()
        months = monthly_data.index.tolist()
        amounts = monthly_data.values.tolist()

        fig2, ax2 = plt.subplots()
        ax2.bar(months, amounts)
        ax2.set_xlabel('Bulan')
        ax2.set_ylabel('Pengeluaran (Rp)')
        ax2.set_title('Pengeluaran Per Bulan')
        fig2.savefig(os.path.join(chart_folder, 'bar_chart.png'))
        plt.close(fig2)
    except Exception as e:
        print(f"Error generating bar chart: {e}")

    print("Grafik berhasil disimpan di folder static/charts.")

if __name__ == '__main__':
    generate_charts()
