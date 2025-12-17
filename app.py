# app.py
import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Marks Analysis", layout="wide")

st.title("📊 Student Marks Analysis Across Academic Years")

# Input CSV link
csv_link = st.text_input("Enter your CSV file link:", "YOUR_CSV_LINK_HERE.csv")

if csv_link:
    try:
        # Load dataset
        data = pd.read_csv(csv_link)
        
        st.subheader("Dataset Preview")
        st.dataframe(data.head())
        
        if "Academic_Year" in data.columns and "Marks" in data.columns:
            # Group marks by Academic Year
            grouped = data.groupby('Academic_Year')['Marks']
            
            # Display statistics
            st.subheader("Statistics by Academic Year")
            stats_data = []
            for year, marks in grouped:
                mean = marks.mean()
                median = marks.median()
                mode = stats.mode(marks)[0][0]
                std_dev = marks.std()
                stats_data.append([year, mean, median, mode, std_dev])
            
            stats_df = pd.DataFrame(stats_data, columns=["Academic Year", "Mean", "Median", "Mode", "Std Dev"])
            st.table(stats_df)
            
            # Visualization
            st.subheader("Marks Distribution by Academic Year")
            fig, ax = plt.subplots(figsize=(8,5))
            data.boxplot(column='Marks', by='Academic_Year', ax=ax)
            ax.set_title('Student Marks by Academic Year')
            ax.set_xlabel('Academic Year')
            ax.set_ylabel('Marks')
            plt.suptitle('')
            st.pyplot(fig)
            
            # Optional: ANOVA test
            st.subheader("ANOVA Test Across Years")
            marks_lists = [marks.values for year, marks in grouped]
            f_val, p_val = stats.f_oneway(*marks_lists)
            st.write(f"F-value: {f_val:.2f}, p-value: {p_val:.4f}")
            if p_val < 0.05:
                st.success("There is a significant difference in marks between years.")
            else:
                st.info("No significant difference in marks between years.")
        else:
            st.error("CSV must contain 'Academic_Year' and 'Marks' columns.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
