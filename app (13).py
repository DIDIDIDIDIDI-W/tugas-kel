import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("Analisis Regresi Sederhana")

# Load data
file_path = '/content/data bengkulu.xlsx'
try:
    df = pd.read_excel(file_path)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
except FileNotFoundError:
    st.error(f"File not found at {file_path}. Please make sure the file exists.")
    st.stop()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Select numerical columns
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_columns) >= 2:
    st.subheader("Konfigurasi Regresi")
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Pilih Variabel Independent (X)", numeric_columns, index=0)
    with col2:
        y_col = st.selectbox("Pilih Variabel Dependent (Y)", numeric_columns, index=min(1, len(numeric_columns)-1))

    if st.button("Jalankan Analisis"):
        X = df[[x_col]].values
        y = df[y_col].values

        # Model
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # Metrics
        r_sq = model.score(X, y)
        
        st.write(f"**Koefisien (Slope):** {model.coef_[0]:.4f}")
        st.write(f"**Intercept:** {model.intercept_:.4f}")
        st.write(f"**R-squared:** {r_sq:.4f}")

        # Plot
        fig, ax = plt.subplots()
        sns.scatterplot(x=X.flatten(), y=y, color='blue', alpha=0.5, label='Data', ax=ax)
        sns.lineplot(x=X.flatten(), y=y_pred, color='red', linewidth=2, label='Regression Line', ax=ax)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"Regresi Linear: {y_col} vs {x_col}")
        ax.legend()
        st.pyplot(fig)
else:
    st.warning("Dataframe tidak memiliki cukup kolom numerik untuk melakukan regresi.")
