import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE_NAME = "expense.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
        df = df.dropna(subset=["date"])

        if "type" not in df.columns:
            df["type"] = "Expense"
    else:
        df = pd.DataFrame(columns=["date", "type", "category", "amount", "description"])
    return df

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

st.set_page_config(page_title="Finance Tracker Dashboard", layout="wide")

st.title("Finance Tracker Dashboard")

df = load_data()

st.sidebar.header("Add New Entry")

date = st.sidebar.date_input("Select Date")
entry_type = st.sidebar.selectbox("Type", ["Expense", "Income"])
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Entry"):
    if category and amount > 0:
        new_row = {
            "date": date,
            "type": entry_type,
            "category": category.title(),
            "amount": amount,
            "description": description
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.sidebar.success("Entry Added Successfully!")
        st.rerun()
    else:
        st.sidebar.error("Please enter valid details.")

st.subheader("All Transactions")
st.dataframe(df)

st.subheader("Overall Summary")
if not df.empty:
    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    savings = total_income - total_expense
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rs.{total_income:.2f}")
    col2.metric("Total Expense", f"Rs.{total_expense:.2f}")
    col3.metric("Total Savings", f"Rs.{savings:.2f}")

st.subheader("Monthly Analysis")

if not df.empty:
    df["year_month"] = df["date"].dt.to_period("M")

    selected_month = st.selectbox(
        "Select Month",
        sorted(df["year_month"].astype(str).unique())
    )

    filtered_df = df[df["year_month"].astype(str) == selected_month]

    month_income = filtered_df[filtered_df["type"] == "Income"]["amount"].sum()
    month_expense = filtered_df[filtered_df["type"] == "Expense"]["amount"].sum()
    month_savings = month_income - month_expense

    st.write(f"Income: Rs.{month_income:.2f}")
    st.write(f"Expense: Rs.{month_expense:.2f}")
    st.write(f"Savings: Rs.{month_savings:.2f}")

    expense_data = filtered_df[filtered_df["type"] == "Expense"]
    pie_data = expense_data.groupby("category")["amount"].sum()

    if not pie_data.empty:
        st.write("Expense Distribution (Pie Chart)")
        fig1 = plt.figure()
        plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
        plt.title("Category-wise Expense Distribution")
        st.pyplot(fig1)

        st.write("Expense Distribution (Bar Chart)")
        fig2 = plt.figure()
        plt.bar(pie_data.index, pie_data.values)
        plt.title("Category-wise Expense Distribution")
        plt.xlabel("Category")
        plt.ylabel("Amount (Rs.)")
        plt.xticks(rotation=60)
        st.pyplot(fig2)
    
    else:
        st.info("No expenses for selected month.")

else:
    st.info("No data available.")
