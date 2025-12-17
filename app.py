# app.py
import streamlit as st
import pandas as pd
from scipy import stats

st.title("Student Marks Analysis")

# CSV link input
csv_link = st.text_input("Enter CSV file link")

if csv_link:
    try:
        # Read CSV
        data = pd.read_csv(csv_link)

        st.subheader("Dataset Preview")
        st.dataframe(data)

        # Group by Academic Year
        st.subheader("Marks Statistics by Academic Year")

        result = []

        for year, marks in data.groupby("Academic_Year")["Marks"]:
            mean = marks.mean()
            median = marks.median()
            mode = stats.mode(marks)[0][0]
            result.append([year, mean, median, mode])

        result_df = pd.DataFrame(
            result,
            columns=["Academic Year", "Mean", "Median", "Mode"]
        )

        st.table(result_df)

    except Exception as e:
        st.error("Error reading CSV file")

