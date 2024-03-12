import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk mengimpor data
@st.cache_data
def load_data():
    data_df = pd.read_csv('day.csv')
    return data_df

# Fungsi untuk melakukan pembersihan data
def clean_data(data_df):
    data_df['season'] = data_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return data_df

# Fungsi untuk menampilkan data wrangling
def data_wrangling(data_df):
    st.subheader("Data Wrangling")
    
    st.subheader("Gathering Data")
    st.write("Berikut merupakan dataset dari Bike Sharing pada skala hari")
    st.write(data_df)

    st.subheader("Assessing Data")
    st.write("Melakukan pemeriksaan parameter statistik menggunakan metode describe()")
    st.write(data_df.describe())

    st.subheader("Cleaning Data")
    st.write("Mengubah nilai dari parameter 'season' menjadi nama musim")
    cleaned_data_df = clean_data(data_df.copy())
    st.write(cleaned_data_df)

# Fungsi untuk menjawab pertanyaan EDA
def eda_questions(data_df):
    st.subheader('Exploratory Data Analysis (EDA)')
    
    st.subheader('Pertanyaan 1')
    st.write("Bagaimana distribusi peminjaman untuk masing-masing musim dan kondisi cuaca?")
    st.write('')
    st.write("Melakukan pemetaan tabel menggunakan pivot table")
    data_df['season'] = data_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    data_musim = data_df.groupby(by=["season", "weathersit"]).agg({
        "casual": "nunique",
        "registered": "nunique"
    })
    st.write(data_musim)
    st.write('Grafik')
    data_musim['total'] = data_musim['casual'] + data_musim['registered']
    fig, ax = plt.subplots()
    sns.barplot(data=data_musim, x="season", y="total", hue="weathersit", errorbar=None, ax=ax)
    st.pyplot(fig)

    st.subheader('Pertanyaan 2')
    st.write("Pengaruh hari kerja/ akhir pekan terhadap peminjaman untuk setiap musim?")
    st.write('')
    st.write("Melakukan pemetaan tabel menggunakan pivot table")
    data_holiday = data_df.groupby(by="season").agg({
        "casual": "nunique",
        "registered": "nunique",
    })
    st.write(data_holiday)
    st.write('Grafik')
    data_holiday['total'] = data_holiday['casual'] + data_holiday['registered']
    fig, ax = plt.subplots()
    sns.scatterplot(data=data_holiday, x='season', y='casual', ax=ax)
    sns.scatterplot(data=data_holiday, x='season', y='registered', ax=ax)
    ax.set_ylim(150, 190)
    st.pyplot(fig)
    
    # Kesimpulan Pertanyaan 1
    st.subheader('Kesimpulan Pertanyaan 1:')
    total_rental_per_season = data_df.groupby('season')[['casual', 'registered']].sum()  # Menggunakan sum untuk mendapatkan jumlah total peminjaman
    st.write("Berdasarkan analisis, terlihat bahwa distribusi peminjaman berbeda-beda untuk setiap musim dan kondisi cuaca.")
    st.write("Total peminjaman untuk masing-masing musim:")
    st.write(total_rental_per_season)
    
    max_season = total_rental_per_season.sum(axis=1).idxmax()  # Menggunakan sum(axis=1) untuk mendapatkan total peminjaman
    min_season = total_rental_per_season.sum(axis=1).idxmin()  # Menggunakan sum(axis=1) untuk mendapatkan total peminjaman
    
    seasons_map = {'Spring': 'Spring (Musim Semi)', 'Summer': 'Summer (Musim Panas)', 'Fall': 'Fall (Musim Gugur)', 'Winter': 'Winter (Musim Dingin)'}
    
    st.write(f"Peminjam terbanyak berada pada {seasons_map[max_season]} dan peminjam paling sedikit berada pada {seasons_map[min_season]}.")
    
    # Kesimpulan Pertanyaan 2
    st.subheader('Kesimpulan Pertanyaan 2:')
    weekday_vs_weekend = data_df.groupby('weekday')['cnt'].sum()
    st.write("Berdasarkan analisis, terdapat hubungan antara hari kerja/akhir pekan dengan jumlah peminjaman untuk setiap musim.")
    st.write("Total peminjaman pada hari kerja vs akhir pekan:")
    st.write(weekday_vs_weekend)
    
    max_day = weekday_vs_weekend.idxmax()
    min_day = weekday_vs_weekend.idxmin()
    
    days_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    
    st.write(f"Peminjam terbanyak berada pada hari {days_map[max_day]} dan peminjam paling sedikit berada pada hari {days_map[min_day]}.")
    
def main():
    st.title('Analisis Data Bike Sharing')
    data_df = load_data()
    
    menu = ["Data Wrangling", "Exploratory Data Analysis (EDA)"]
    choice = st.sidebar.selectbox("Pilihan Menu", menu)

    if choice == "Data Wrangling":
        data_wrangling(data_df)
    elif choice == "Exploratory Data Analysis (EDA)":
        eda_questions(data_df)
        
    if __name__ == "__main__":
        main() 
