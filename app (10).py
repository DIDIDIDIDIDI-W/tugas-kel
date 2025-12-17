import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def main():
    st.title('Analisis Regresi Harga Beras')

    # 3. Implement data loading
    @st.cache_data
    def load_data(file_path):
        df = pd.read_excel(file_path)
        return df

    df = load_data('/content/Tabel Harga Berdasarkan Daerah JAWA TENGAH.xlsx')
    
    st.subheader('Data Harga Beras (5 Baris Pertama)')
    st.dataframe(df.head())

    # 4. Implement data cleaning
    date_columns = df.columns[2:]
    for col in date_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '.', regex=False).astype(float)

    rice_types_for_analysis = [
        'Beras Kualitas Bawah I',
        'Beras Kualitas Bawah II',
        'Beras Kualitas Medium I',
        'Beras Kualitas Medium II'
    ]

    df_filtered = df[df['Komoditas (Rp)'].isin(rice_types_for_analysis)].copy()
    df_filtered.set_index('Komoditas (Rp)', inplace=True)
    df_transposed = df_filtered[date_columns].T
    df_transposed.index.name = 'Date'

    # 5. Identify variables
    dependent_variable = 'Beras Kualitas Bawah I'
    Y = df_transposed[dependent_variable]
    independent_variables = [col for col in df_transposed.columns if col != dependent_variable]
    X = df_transposed[independent_variables]

    st.subheader(f'Variabel Dependen: {dependent_variable}')
    st.subheader('Variabel Independen:')
    st.write(independent_variables)

    # 6. Perform multiple regression
    X_with_constant = sm.add_constant(X)
    model = sm.OLS(Y, X_with_constant)
    model_results = model.fit()

    # 7. Display regression results
    st.subheader('Ringkasan Hasil Regresi Berganda')
    st.text(model_results.summary().as_text())

    # 8. Visualize regression outcomes
    st.subheader('Visualisasi Hasil Regresi: Aktual vs. Prediksi')
    Y_pred = model_results.predict(X_with_constant)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(Y, Y_pred, alpha=0.7, label='Aktual vs. Prediksi')

    min_val = min(Y.min(), Y_pred.min())
    max_val = max(Y.max(), Y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Prediksi Sempurna')

    ax.set_xlabel('Nilai Aktual')
    ax.set_ylabel('Nilai Prediksi')
    ax.set_title('Aktual vs. Prediksi Harga Beras Kualitas Bawah I')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.success("Analisis Regresi Selesai!")

if __name__ == '__main__':
    main()
