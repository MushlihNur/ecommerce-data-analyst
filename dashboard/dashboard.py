import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Fungsi untuk memuat data
def load_data():
    # Ganti "all_data.csv" dengan path ke data Anda
    all_df = pd.read_csv("dashboard/all_data.csv")
    all_df = all_df[['customer_city', 'customer_state', 'customer_unique_id', 'product_category_name_english', 'review_score', 'order_item_id']].drop_duplicates()
    return all_df

# Load data
all_df = load_data()

# Sidebar
view_type = st.sidebar.radio(
    "Pilih Tampilan:", 
    options=["Analisis Geografis Pelanggan", "Analisis Kategori Produk", "Analisis Ulasan dan Penjualan"]
)

# Halaman Utama
st.title("Dashboard E-Commerce Data Analyst")
st.write("Dashboard ini menunjukkan hasil analisis dari data E-Commerce")

# Hitung konsentrasi pelanggan
city_customer_count = all_df.groupby('customer_city')['customer_unique_id'].nunique().reset_index()
city_customer_count.columns = ['customer_city', 'customer_count']
state_customer_count = all_df.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
state_customer_count.columns = ['customer_state', 'customer_count']

# Mengurangi jumlah kota untuk visualisasi yang lebih cepat
top_cities = city_customer_count.nlargest(100, 'customer_count')

if view_type == "Analisis Geografis Pelanggan":
    st.title("Analisis Geografis Pelanggan")

    # Analisis kota
    st.subheader("Top Kota dengan Jumlah Pelanggan Terbanyak")
    top_cities = city_customer_count.nlargest(10, 'customer_count')

    # Bar Chart Kota
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='customer_count', y='customer_city', data=top_cities, palette='coolwarm', ax=ax)
    ax.set_title("Top 10 Kota dengan Konsentrasi Pelanggan")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Kota")
    st.pyplot(fig)

    # Tampilkan tabel data kota
    st.write("Tabel Data Kota dengan Konsentrasi Pelanggan Tertinggi:")
    st.dataframe(top_cities)

    # Analisis negara bagian
    st.subheader("Top Negara Bagian dengan Jumlah Pelanggan Terbanyak")
    top_states = state_customer_count.nlargest(10, 'customer_count')

    # Bar Chart Negara Bagian
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='customer_count', y='customer_state', data=top_states, palette='viridis', ax=ax)
    ax.set_title("Top 10 Negara Bagian dengan Konsentrasi Pelanggan")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Negara Bagian")
    st.pyplot(fig)

    # Tampilkan tabel data negara bagian
    st.write("Tabel Data Negara Bagian dengan Konsentrasi Pelanggan Tertinggi:")
    st.dataframe(top_states)

elif view_type == "Analisis Kategori Produk":
    st.title("Analisis Kategori Produk")

    # Hitung jumlah produk per kategori
    product_category_sales_df = all_df['product_category_name_english'].value_counts()
    product_category_sales_df = product_category_sales_df.rename_axis('product_category_name').reset_index(name='product_count')
    st.write('Jumlah Produk per Kategori:')
    st.dataframe(product_category_sales_df)

    # Hitung persentase produk per kategori
    product_category_percent_df = all_df['product_category_name_english'].value_counts(normalize=True) * 100
    product_category_percent_df = product_category_percent_df.rename_axis('product_category_name').reset_index(name='percentage')
    st.write('Persentase Produk per Kategori:')
    st.dataframe(product_category_percent_df)

    # Pie chart untuk persentase produk per kategori
    st.subheader("Persentase Produk per Kategori")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(product_category_percent_df['percentage'], labels=product_category_percent_df['product_category_name'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title("Persentase Produk per Kategori")
    st.pyplot(fig)

    # Bar chart jumlah produk per kategori
    st.subheader("Jumlah Produk per Kategori")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='product_category_name', y='product_count', data=product_category_sales_df, ax=ax, palette='Set2')
    ax.set_title("Jumlah Produk per Kategori")
    ax.set_xlabel("Kategori Produk")
    ax.set_ylabel("Jumlah Produk")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

elif view_type == "Analisis Ulasan dan Penjualan":
    st.title("Analisis Hubungan Ulasan Pelanggan dan Jumlah Produk Terjual")

    # Pastikan data memiliki kolom review_score dan order_item_id
    if 'review_score' in all_df.columns and 'order_item_id' in all_df.columns:
        # Grupkan data berdasarkan review_score
        product_sales_df = all_df.groupby('review_score')['order_item_id'].count().reset_index()
        product_sales_df.columns = ['review_score', 'product_sales']

        # Tampilkan tabel data
        st.write("Jumlah Produk Terjual Berdasarkan Rating Ulasan:")
        st.dataframe(product_sales_df)

        # Bar Chart
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='review_score', y='product_sales', data=product_sales_df, palette='coolwarm', ax=ax)
        ax.set_title("Hubungan antara Ulasan Pelanggan (Rating) dan Jumlah Produk yang Terjual")
        ax.set_xlabel("Ulasan Pelanggan (Rating)")
        ax.set_ylabel("Jumlah Produk Terjual")
        st.pyplot(fig)

        # Hitung korelasi
        correlation_rating_product = product_sales_df['review_score'].corr(product_sales_df['product_sales'])
        st.write(f"Korelasi antara Ulasan Pelanggan dan Jumlah Produk Terjual: **{round(correlation_rating_product, 2)}**")
    else:
        st.write("Data tidak memiliki kolom 'review_score' atau 'order_item_id' yang diperlukan untuk analisis ini.")
