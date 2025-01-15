import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Fungsi untuk memuat data
def load_data():
    # Ganti "data/all_data.csv" dengan path ke data Anda
    all_df = pd.read_csv("data/all_data.csv")
    all_df = all_df[['customer_city', 'customer_state', 'customer_unique_id', 'product_category_name_english']].drop_duplicates()
    return all_df

# Load data
all_df = load_data()

# Sidebar
view_type = st.sidebar.radio(
    "Pilih Tampilan:", 
    options=["Top Kota", "Top Negara Bagian", "Peta Geografis", "Analisis Kategori Produk"]
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

if view_type == "Top Kota":
    st.title("Top Kota dengan Jumlah Pelanggan Terbanyak")

    # Ambil 10 kota dengan pelanggan terbanyak
    top_cities = city_customer_count.nlargest(10, 'customer_count')

    # Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='customer_count', y='customer_city', data=top_cities, palette='coolwarm', ax=ax)
    ax.set_title("Tok 10 Kota dengan Konsentrasi Pelanggan")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Kota")
    st.pyplot(fig)

    # Tampilkan tabel data
    st.write("Tabel Data Kota dengan Konsentrasi Pelanggan Tertinggi:")
    st.dataframe(top_cities)

elif view_type == "Top Negara Bagian":
    st.title("Top Negara Bagian dengan Jumlah Pelanggan Terbanyak")

    # Ambil 10 negara bagian dengan pelanggan terbanyak
    top_states = state_customer_count.nlargest(10, 'customer_count')

    # Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='customer_count', y='customer_state', data=top_states, palette='viridis', ax=ax)
    ax.set_title("Tok 10 Negara Bagian dengan Konsentrasi Pelanggan")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Negara Bagian")
    st.pyplot(fig)

    # Tampilkan tabel data
    st.write("Tabel Data Negara Bagian dengan Konsentrasi Pelanggan Tertinggi:")
    st.dataframe(top_states)

elif view_type == "Peta Geografis":
    st.title("Peta Geografis Konsentrasi Pelanggan")

    geolocation_df = pd.read_csv("data/geolocation_dataset.csv")
    city_coordinates = geolocation_df[['geolocation_city', 'geolocation_lat', 'geolocation_lng']]
    city_coordinates.columns = ['customer_city', 'latitude', 'longitude']

    # Gabungkan data kota dengan koordinat, hanya ambil kota yang relevan
    city_data = pd.merge(
        top_cities,
        city_coordinates,
        on='customer_city',
        how='inner',
    )

    # Pastikan tidak ada nilai kosong (drop NaN)
    city_data = city_data.dropna(subset=['latitude', 'longitude'])

    # Peta menggunakan Plotly
    fig = px.scatter_mapbox(
        city_data,
        lat="latitude",
        lon="longitude",
        size="customer_count",
        hover_name="customer_city",
        color="customer_count",
        color_continuous_scale=px.colors.sequential.Blues,
        size_max=30,
        zoom=4,
        mapbox_style="open-street-map",
        title="Peta Konsentrasi Pelanggan Berdasarkan Kota"
    )
    st.plotly_chart(fig)

    # Tampilkan tabel data kota dengan koordinat
    st.write("Tabel Data Kota dengan Konsentrasi Pelanggan dan Koordinat:")
    st.dataframe(city_data)

elif view_type == "Analisis Kategori Produk":
    st.title("Analisis Kategori Produk")

    # Hitung jumlah produk per kategori
    product_category_sales_df = all_df['product_category_name_english'].value_counts()
    st.write('Jumlah Produk per Kategori:')
    st.dataframe(product_category_sales_df)

    # Hitung persentase produk per kategori
    product_category_percent_df = all_df['product_category_name_english'].value_counts(normalize=True) * 100
    st.write('Persentase Produk per Kategori:')
    st.dataframe(product_category_percent_df)

    # Pie chart untuk persentase produk per kategori
    st.subheader("Persentase Produk per Kategori")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(product_category_percent_df, labels=product_category_percent_df.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title("Persentase Produk per Kategori")
    st.pyplot(fig)

    # Bar chart jumlah produk per kategori
    st.subheader("Jumlah Produk per Kategori")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=product_category_sales_df.index, y=product_category_sales_df.values, ax=ax, palette='Set2')
    ax.set_title("Jumlah Produk per Kategori")
    ax.set_xlabel("Kategori Produk")
    ax.set_ylabel("Jumlah Produk")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)