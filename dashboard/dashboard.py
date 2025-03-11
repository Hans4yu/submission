import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

file_path = 'dashboard/main_data.csv'

try:
    main_df = pd.read_csv(file_path)
    if 'order_purchase_timestamp' in main_df.columns:
        main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])
except FileNotFoundError:
    st.error(f"Error: File '{file_path}' not found. Please ensure the file exists in the specified path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while reading the file: {e}")
    st.stop()

st.title("E-Commerce Sales Dashboard")

if st.checkbox("Show Dataset"):
    st.write(main_df)

st.sidebar.header("Filters")

if 'order_purchase_timestamp' in main_df.columns:
    min_date = main_df['order_purchase_timestamp'].min().date()
    max_date = main_df['order_purchase_timestamp'].max().date()
    selected_date_range = st.sidebar.date_input("Select date range", [min_date, max_date])
    start_date, end_date = selected_date_range
else:
    st.warning("The dataset needs a 'order_purchase_timestamp' column to create date filter.")
    start_date, end_date = None, None

if 'payment_value' in main_df.columns: 
    min_revenue = st.sidebar.number_input("Minimum Revenue", min_value=0.0, value=0.0)
    max_revenue = st.sidebar.number_input("Maximum Revenue", min_value=0.0, value=main_df['payment_value'].max())
else:
    min_revenue, max_revenue = 0, 0
    st.warning("The dataset needs a 'payment_value' column to create revenue filters.")

if 'product_category_name_english' in main_df.columns:
    selected_category = st.sidebar.multiselect(
        "Select product categories",
        main_df['product_category_name_english'].unique(),
        default=main_df['product_category_name_english'].unique()
    )
else:
    selected_category = []
    st.warning("product_category_name_english column not found")

filtered_df = main_df.copy()

if start_date and end_date and 'order_purchase_timestamp' in main_df.columns:
    filtered_df = filtered_df[
        (filtered_df['order_purchase_timestamp'].dt.date >= start_date) &
        (filtered_df['order_purchase_timestamp'].dt.date <= end_date)
    ]

if 'payment_value' in main_df.columns:
    filtered_df = filtered_df[
        (filtered_df['payment_value'] >= min_revenue) &
        (filtered_df['payment_value'] <= max_revenue)
    ]

if selected_category and 'product_category_name_english' in main_df.columns:
    filtered_df = filtered_df[filtered_df['product_category_name_english'].isin(selected_category)]

st.write(filtered_df)

if 'order_purchase_timestamp' in filtered_df.columns and 'order_id' in filtered_df.columns:
    daily_sales = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.date)['order_id'].count()
    st.subheader("Daily Sales (Filtered)")
    st.line_chart(daily_sales)

st.header("Sales & Revenue Performance (Last Month)")
if 'order_purchase_timestamp' in main_df.columns and 'order_id' in main_df.columns:
    try:
        last_month = main_df['order_purchase_timestamp'].max() - pd.DateOffset(months=1)
        last_month_data = main_df[main_df['order_purchase_timestamp'] >= last_month]
        daily_sales = last_month_data.groupby(last_month_data['order_purchase_timestamp'].dt.date)['order_id'].count()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_sales.index, daily_sales.values)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Sales')
        ax.set_title('Daily Sales Performance (Last Month)')
        st.pyplot(fig)

        st.write("""
        **Deskripsi Grafik:**

        Grafik ini menampilkan performa penjualan harian selama sebulan terakhir, dari tanggal 29 Juli 2018 hingga 29 Agustus 2018. 

        **Tren Utama:**

        * **Awal Bulan (29 Juli - 6 Agustus):** Terjadi peningkatan penjualan yang signifikan. Penjualan mencapai puncaknya di sekitar tanggal 5-6 Agustus, dengan jumlah penjualan melebihi 400 unit.
        * **Pertengahan Bulan (6 Agustus - 17 Agustus):** Setelah mencapai puncak, terjadi penurunan penjualan secara bertahap. Namun, penjualan tetap berada di atas 200 unit.
        * **Akhir Bulan (17 Agustus - 29 Agustus):** Terjadi penurunan penjualan yang tajam dan konsisten. Penjualan turun drastis, mencapai di bawah 100 unit pada akhir bulan.

        **Analisis:**

        * Grafik ini menunjukkan adanya fluktuasi penjualan yang signifikan sepanjang bulan.
        * Peningkatan penjualan di awal bulan mungkin disebabkan oleh promosi khusus, peluncuran produk baru, atau faktor musiman.
        * Penurunan penjualan di akhir bulan mengindikasikan adanya tren penurunan yang perlu diinvestigasi lebih lanjut. Faktor-faktor seperti perubahan permintaan pasar, persaingan yang meningkat, atau masalah internal mungkin menjadi penyebabnya.

        **Kesimpulan:**

        Grafik ini memberikan gambaran visual yang jelas tentang performa penjualan harian selama sebulan terakhir. Informasi ini dapat digunakan untuk mengidentifikasi tren penjualan, memahami fluktuasi pasar, dan mengambil keputusan bisnis yang lebih baik.
        """)
        
        daily_revenue = last_month_data.groupby(last_month_data['order_purchase_timestamp'].dt.date)['payment_value'].sum()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_revenue.index, daily_revenue.values)
        ax.set_xlabel('Date')
        ax.set_ylabel('Revenue')
        ax.set_title('Daily Revenue Performance (Last Month)')
        st.pyplot(fig)
        st.write("""
        **Deskripsi Grafik:**

        Grafik ini menampilkan performa pendapatan harian selama sebulan terakhir, dari tanggal 29 Juli 2018 hingga 29 Agustus 2018.

        **Tren Utama:**

        * **Awal Bulan (29 Juli - 6 Agustus):** Terjadi peningkatan pendapatan yang signifikan. Pendapatan mencapai puncaknya di sekitar tanggal 6 Agustus, dengan nilai pendapatan melebihi 80,000 unit mata uang.
        * **Pertengahan Bulan (6 Agustus - 17 Agustus):** Setelah mencapai puncak, terjadi penurunan pendapatan secara bertahap. Namun, pendapatan tetap berada di atas 30,000 unit mata uang.
        * **Akhir Bulan (17 Agustus - 29 Agustus):** Terjadi penurunan pendapatan yang tajam dan konsisten. Pendapatan turun drastis, mencapai di bawah 10,000 unit mata uang pada akhir bulan.

        **Analisis:**

        * Grafik ini menunjukkan adanya fluktuasi pendapatan yang signifikan sepanjang bulan.
        * Peningkatan pendapatan di awal bulan mungkin disebabkan oleh promosi khusus, peluncuran produk baru, atau faktor musiman seperti hari libur atau akhir pekan.
        * Penurunan pendapatan di akhir bulan mengindikasikan adanya tren penurunan yang perlu diinvestigasi lebih lanjut. Faktor-faktor seperti perubahan permintaan pasar, persaingan yang meningkat, atau masalah internal mungkin menjadi penyebabnya.
        * Terdapat beberapa fluktuasi kecil di pertengahan bulan, yang mungkin disebabkan oleh variasi harian dalam volume penjualan.

        **Kesimpulan:**

        Grafik ini memberikan gambaran visual yang jelas tentang performa pendapatan harian selama sebulan terakhir. Informasi ini dapat digunakan untuk mengidentifikasi tren pendapatan, memahami fluktuasi pasar, dan mengambil keputusan bisnis yang lebih baik. Misalnya, perusahaan dapat menyelidiki penyebab penurunan pendapatan di akhir bulan dan mengambil tindakan untuk meningkatkan penjualan.
        """)

    except KeyError:
        st.error("Error: 'order_purchase_timestamp' or 'order_id' column not found in the dataset. Please verify the column names.")
else:
    st.warning("The dataset needs 'order_purchase_timestamp' and 'order_id' columns to create this chart.")

 
st.header("Product Performance vs. Price")

if {'product_category_name_english', 'price', 'payment_value'}.issubset(main_df.columns):
    try:
        # Calculate revenue per product category
        product_revenue = main_df.groupby('product_category_name_english')['payment_value'].sum()

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(main_df['price'], main_df['payment_value'], alpha=0.5)  # Scatter plot
        ax.set_xlabel('Price')
        ax.set_ylabel('Revenue')
        ax.set_title('Product Performance vs. Price')

        # Add a trendline (optional)
        # You might want to explore other regression methods for a better fit.
        z = np.polyfit(main_df['price'], main_df['payment_value'], 1)
        p = np.poly1d(z)
        ax.plot(main_df['price'],p(main_df['price']),"r--")

        st.pyplot(fig)
        
        st.write("""
        **Deskripsi Grafik:**

        Grafik ini menampilkan hubungan antara harga produk (Price) dan pendapatan yang dihasilkan (Revenue), dengan fokus pada rentang data.

        **Rentang Data:**

        * **Harga (Price):** Harga produk bervariasi dari 0 hingga hampir 7000 unit mata uang. Sebagian besar produk memiliki harga di bawah 2000 unit mata uang.
        * **Pendapatan (Revenue):** Pendapatan produk bervariasi dari 0 hingga lebih dari 14000 unit mata uang. Sebagian besar produk menghasilkan pendapatan di bawah 2000 unit mata uang.

        **Tren Utama:**

        * **Hubungan Positif:** Terdapat tren umum bahwa produk dengan harga lebih tinggi cenderung menghasilkan pendapatan lebih tinggi. Garis regresi linear merah menunjukkan tren positif ini.
        * **Sebaran Data:** Data tersebar luas, menunjukkan bahwa terdapat variasi besar dalam pendapatan untuk produk dengan harga yang sama.
        * **Outliers:** Terdapat beberapa produk dengan pendapatan sangat tinggi (di atas 10000 unit mata uang) meskipun harganya tidak terlalu tinggi (di bawah 2000 unit mata uang). Produk-produk ini dapat dianggap sebagai outliers.

        **Analisis:**

        * Rentang harga menunjukkan bahwa platform e-commerce ini menawarkan berbagai produk dengan harga yang berbeda.
        * Rentang pendapatan menunjukkan bahwa terdapat variasi besar dalam kinerja produk.
        * Outliers menunjukkan bahwa faktor lain selain harga mempengaruhi pendapatan produk.

        **Kesimpulan:**

        Grafik ini memberikan gambaran visual tentang rentang harga dan pendapatan produk, serta hubungan antara keduanya. Informasi ini dapat digunakan untuk:

        * Memahami distribusi harga dan pendapatan produk.
        * Mengidentifikasi produk dengan kinerja terbaik dan terburuk.
        * Mengambil keputusan tentang penetapan harga dan strategi pemasaran.
        """)
    except KeyError as e:
        st.error(f"Error: Column '{e}' not found in the dataset. Please verify the column names.")
else:
    st.warning("The dataset needs 'product_category_name_english', 'price', and 'payment_value' columns to create this chart.")


st.header("Top 5 Highest/Lower Selling Category Products")

if 'product_category_name_english' in main_df.columns and 'order_id' in main_df.columns:
    try:
        product_sales = main_df.groupby('product_category_name_english')['order_id'].count()
        top_products = product_sales.nlargest(5)
        bottom_products = product_sales.nsmallest(5)

        st.subheader("Top 5 Products")
        fig_top, ax_top = plt.subplots(figsize=(8, 5))
        top_products.plot(kind='bar', ax=ax_top, title='Top Selling Products')
        ax_top.set_xlabel('Product Category')
        ax_top.set_ylabel('Number of Sales')
        st.pyplot(fig_top)
        st.write("""
        **Grafik Kiri (Produk Kategori Penjualan Tertinggi):**

        * Grafik ini menampilkan lima kategori produk dengan jumlah penjualan terbanyak.
        * Kategori-kategori tersebut adalah:
            * bed_bath_table
            * health_beauty
            * sports_leisure
            * furniture_decor
            * computers_accessories
        * Grafik menggunakan batang vertikal untuk merepresentasikan jumlah penjualan setiap kategori.
        * Kategori "bed_bath_table" memiliki penjualan tertinggi, diikuti oleh "health_beauty".
        """)

        st.subheader("Bottom 5 Products")
        fig_bottom, ax_bottom = plt.subplots(figsize=(8, 5))
        bottom_products.plot(kind='bar', ax=ax_bottom, title='Bottom Selling Products')
        ax_bottom.set_xlabel('Product Category')
        ax_bottom.set_ylabel('Number of Sales')
        st.pyplot(fig_bottom)
        st.write("""
        **Grafik Kanan (Produk Kategori Penjualan Terendah):**

        * Grafik ini menampilkan lima kategori produk dengan jumlah penjualan paling sedikit.
        * Kategori-kategori tersebut adalah:
            * security_and_services
            * fashion_childrens_clothes
            * cds_dvds_musicals
            * la_cuisine
            * arts_and_craftmanship
        * Grafik ini juga menggunakan batang vertikal untuk merepresentasikan jumlah penjualan setiap kategori.
        * Kategori "security_and_services" memiliki penjualan terendah, sementara "arts_and_craftmanship" memiliki penjualan tertinggi di antara lima kategori terendah.
        """)

        st.write("""
        **Kesimpulan Umum:**

        * Gambar ini secara visual membandingkan kategori produk dengan kinerja penjualan terbaik dan terburuk.
        * Informasi ini memberikan wawasan tentang popularitas dan permintaan produk di platform e-commerce tersebut.""")
    except KeyError:
        st.error("Error: 'product_category_name_english' or 'order_id' column not found in the dataset. Please verify the column names.")
else:
    st.warning("The dataset needs both 'product_category_name_english"" and 'order_id' columns to create this chart.")
   