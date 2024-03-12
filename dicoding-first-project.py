import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk mengimpor data
@st.cache
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
    sns.barplot(data=data_musim, x="season", y="total", hue="weathersit", errorbar=None)
    st.pyplot()

    st.subheader('Pertanyaan 2')
    st.write("Pengaruh hari terhadap peminjaman untuk setiap musim?")
    st.write('')
    st.write("Melakukan pemetaan tabel menggunakan pivot table")
    data_holiday = data_df.groupby(by="season").agg({
        "casual": "nunique",
        "registered": "nunique",
    })
    st.write(data_holiday)
    st.write('Mengidentifikasi relationship menggunakan correlation')
    st.write(data_holiday.corr())
    st.write('Grafik')
    data_holiday['total'] = data_holiday['casual'] + data_holiday['registered']
    sns.scatterplot(data=data_holiday, x='season', y='casual')
    sns.scatterplot(data=data_holiday, x='season', y='registered')
    plt.ylim(150, 190)
    st.pyplot()

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
