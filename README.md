# E-Commerce Sales Dashboard 🚀

## Deskripsi
Dashboard ini menampilkan analisis data penjualan e-commerce menggunakan Streamlit. Dengan fitur filtering dan visualisasi, pengguna dapat memahami tren penjualan berdasarkan tanggal, kategori produk, dan pendapatan.

## Setup Environment - Anaconda
```
conda create --name ecommerce-dashboard python=3.9
conda activate ecommerce-dashboard
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir ecommerce_dashboard
cd ecommerce_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit
```
cd submission_tes/dashboard
streamlit run dashboard.py
```

## Struktur Folder
```
submission_tes/
│── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│── data/
│   ├── product_category_name_translation.csv
│   ├── sellers_dataset.csv
│── notebook.ipynb
│── README.md
│── requirements.txt
```

