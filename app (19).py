
import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Harga Pangan Bengkulu", layout="wide")

# Judul Utama
st.title(' Data Harga Komoditas Pangan di Provinsi Bnegkulu ')
st.markdown("""perkembangan harga pangan strategis di wilayah Bengkulu.
Data ini diambil dari laporan bulanan dan divisualisasikan untuk membantu memantau tren kenaikan atau penurunan harga yang terjadi Di Bengkulu dan Data Yang di ambil 
Berupa Harga Pangan Mulai dari , Beras , Daging Ayam , Daging Sapi , Bawang Merah , Cabe Rawit , Minyak Goreng , Gula Pasir .
""")

# Load data CSV (Bukan Excel lagi)
file_path = 'data_bengkulu.csv'

try:
    # Membaca CSV (Tidak butuh openpyxl)
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Process 'tahun' column
    # Pastikan format tanggal sesuai. CSV kadang mengubah format string, jadi kita parse ulang dengan hati-hati
    df['tahun_date'] = pd.to_datetime(df['tahun'].astype(str).str.replace(' ', ''), format='%m/%Y', errors='coerce')

    # Sidebar untuk filter
    st.sidebar.header("Filter Tampilan")
    show_table = st.sidebar.checkbox("Tampilkan Tabel Data", value=True)

    if show_table:
        st.subheader(" Data Lengkap")
        st.dataframe(df)
        st.caption(f"Menampilkan total {len(df)} baris data.")

    # Plotting Section
    st.divider()
    st.header(" Analisis Harga pangan dari tahun 2019- 2024 di wilayah Bengkulu")
    st.markdown("Grafik ini menunjukkan harga komoditas pangan dari waktu ke waktu mulai Dari Tahun 2019-2024.")

    target_komoditas = ['Beras', 'Daging Ayam', 'Daging Sapi', 'Bawang Merah',
                        'Cabai Rawit', 'Minyak Goreng', 'Gula Pasir']

    # Filter columns that exist in the dataframe
    komoditas_plot = [col for col in target_komoditas if col in df.columns]

    if komoditas_plot:
        selected_commodities = st.multiselect(
            "Pilih Komoditas untuk Ditampilkan:",
            options=komoditas_plot,
            default=komoditas_plot
        )

        if selected_commodities:
            # Native Streamlit Chart
            chart_data = df.set_index('tahun_date')[selected_commodities]
            
            st.subheader("Harga Komoditas Pangan di Bengkulu ")
            st.line_chart(chart_data)

            st.info("""
            ** penjelasan:**
            *   **Beras**: dari tahun 2019 samapai 2022 harganya stabil dan aman aman aja tapi ketika memasuki  tahun 2023 sampai 2024 harganya naik bisa di liaht dari garisnya yang naik tandanya harga udah makin mahal entah kenapa dah  .
            
            *   **Cabai Rawit**: Garis ini paling banyak membentuk pola gunung atau puncak yang tajam dan tidak stabil (volatile). Ini ciri khas Cabai Rawit atau Cabai Merah. Harganya sangat bergantung pada cuaca. Kalau hujan terus dan petani gagal panen, harganya langsung "terbang" ke atas. Tapi begitu panen raya, harganya bisa jatuh sejatuh-jatuhnya.
            
            *   **Daging Ayam**: Garis ini posisinya ada di tengah-tengah, tidak terlalu bawah tapi tidak setinggi daging sapi Harganya fluktuatif mengikuti harga pakan ternak dan permintaan pasar (seperti saat hajatan atau bulan puasa), tapi pemerintah biasanya lebih cepat turun tangan kalau garis ini mulai naik terlalu tinggi..
            
            *   **Minyak Goreng**:harganya cenderung setabil di dari tahun ke tahun tapi ada garis yang naiik di tahun 2022 penyebabnya paska covid 19.
            
            *   **bawang merah**: Garis ini seringkali naik mengikuti pergerakan garis merah muda, tapi tidak setinggi itu. Lincah dan fluktuatif, tapi masih di level harga menengah. Bisa jadi ini adalah kelompok Bawang Merah atau Bawang Putih. Mereka punya pola musiman yang mirip dengan cabai, sering naik barengan terutama menjelang hari raya atau saat distribusi lagi terganggu.
            
            *   **gula pasir **: hampir sama seperti beras yang naik dikit dikit setiap tahun
            
            *   **daging sapi**: Garis hijau di paling atas itu ibaratnya adalah komoditas Daging Sapi. Harganya memang tinggi, tapi dia "anteng" alias stabil. tapi sekalinya naik (seperti yang terlihat di tengah grafik)
            
            *   **kesimpulan**:Umum Grafik Dualisme Harga: Pasar terbagi dua. Ada kelompok komoditas "Elit" (garis hijau) yang harganya tinggi tapi stabil, namun sangat bergejolak.  Terjadi pola lonjakan yang hampir selalu berulang di periode akhir tahun (Desember) dan awal tahun (Februari). Ini menandakan adanya pengaruh besar dari siklus cuaca dan hari raya keagamaan. Meskipun banyak guncangan (lonjakan tajam), harga cenderung kembali ke titik keseimbangan asalnya. Namun, secara jangka panjang, "lantai harga" (harga terendah) pelan-pelan merangkak naik akibat inflasi. .            """)
        else:
            st.warning("Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")

    else:
        st.error("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.text("Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan app.py di GitHub.")
