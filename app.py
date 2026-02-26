import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_NAME = "expense.csv"

# Load data
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
    else:
        df = pd.DataFrame(columns=["date", "type", "category", "amount", "description"])

    return df


# Save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)


# Page config
st.set_page_config(page_title="Finance Tracker Dashboard", layout="wide")
st.title("Finance Tracker Dashboard")

# Load fresh data every run
df = load_data()

# Add entry
st.sidebar.header("Add New Entry")

with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("Select Date")
    entry_type = st.selectbox("Type", ["Expense", "Income"])
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Entry")

if submitted:
    if category.strip() != "" and amount > 0:

        new_entry = pd.DataFrame([{
            "date": str(date),   # Always store as string
            "type": entry_type,
            "category": category.title(),
            "amount": float(amount),
            "description": description
        }])

        # ALWAYS reload latest CSV before appending
        latest_df = load_data()

        updated_df = pd.concat([latest_df, new_entry], ignore_index=True)

        save_data(updated_df)

        st.sidebar.success("Entry Added Successfully!")
        st.rerun()

    else:
        st.sidebar.error("Please enter valid details.")


# Reload data AFTER potential save
df = load_data()

# Convert types safely
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Show data
st.subheader("All Transactions")
st.dataframe(df.sort_values("date", ascending=False))


# Summary
if not df.empty:

    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    savings = total_income - total_expense

    st.subheader("Overall Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rs. {total_income:.2f}")
    col2.metric("Total Expense", f"Rs. {total_expense:.2f}")
    col3.metric("Total Savings", f"Rs. {savings:.2f}")


# Monthly analysis
st.subheader("Monthly Analysis")

if not df.empty:

    df["year_month"] = df["date"].dt.to_period("M")
    months = sorted(df["year_month"].astype(str).dropna().unique())

    if months:
        selected_month = st.selectbox("Select Month", months)

        filtered_df = df[df["year_month"].astype(str) == selected_month]

        month_income = filtered_df[filtered_df["type"] == "Income"]["amount"].sum()
        month_expense = filtered_df[filtered_df["type"] == "Expense"]["amount"].sum()
        month_savings = month_income - month_expense

        st.write(f"#### Income: Rs. {month_income:.2f}")
        st.write(f"#### Expense: Rs. {month_expense:.2f}")
        st.write(f"#### Savings: Rs. {month_savings:.2f}")

        expense_data = filtered_df[filtered_df["type"] == "Expense"]
        pie_data = expense_data.groupby("category")["amount"].sum()

        if not pie_data.empty:

            fig1 = plt.figure()
            plt.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
            plt.title("Category-wise Expense Distribution")
            st.pyplot(fig1)

            fig2 = plt.figure()
            plt.bar(pie_data.index, pie_data.values)
            plt.xticks(rotation=45)
            plt.xlabel("Category")
            plt.ylabel("Amount (Rs.)")
            plt.title("Category-wise Expense Distribution")
            st.pyplot(fig2)

        else:
            st.info("No expenses for selected month.")

else:
    st.info("No data available.")