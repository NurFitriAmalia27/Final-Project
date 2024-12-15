import matplotlib.pyplot as plt
import os
import pymysql
import pandas as pd

# Fungsi untuk mengambil data dari database
def get_data_from_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysql123',  
        database='keuangandb'
    )
    
    query = "SELECT month, category, amount FROM transactions"
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df

# Fungsi untuk menghasilkan grafik pengeluaran per kategori dan per bulan
def generate_charts():
    df = get_data_from_db()
    
    # Data kategori
    category_data = df.groupby('category')['amount'].sum()
    categories = category_data.index.tolist()
    amounts = category_data.values.tolist()

    # Data pengeluaran bulanan
    monthly_data = df.groupby('month')['amount'].sum()
    months = monthly_data.index.tolist()
    monthly_expenses = monthly_data.values.tolist()

    # Membuat grafik pie (persentase pengeluaran per kategori)
    fig1, ax1 = plt.subplots()
    ax1.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  
    
    pie_chart_path = os.path.join('static', 'charts', 'pie_chart.png')
    fig1.savefig(pie_chart_path)

    # Membuat grafik batang (pengeluaran per bulan)
    fig2, ax2 = plt.subplots()
    ax2.bar(months, monthly_expenses)
    ax2.set_xlabel('Bulan')
    ax2.set_ylabel('Pengeluaran (Rp)')
    ax2.set_title('Pengeluaran Per Bulan')

    bar_chart_path = os.path.join('static', 'charts', 'bar_chart.png')
    fig2.savefig(bar_chart_path)

    plt.close(fig1)
    plt.close(fig2)
