import streamlit as st
import pandas as pd
import os

FILE_NAME = "expense.csv"

# ---------------- LOAD DATA ----------------
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
    else:
        df = pd.DataFrame(columns=["id", "date", "type", "category", "amount", "description"])

    # Ensure ID column exists
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))

    return df


# ---------------- SAVE DATA ----------------
def save_data(df):
    df.to_csv(FILE_NAME, index=False)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Finance Tracker Dashboard", layout="wide")
st.title("Finance Tracker Dashboard")

df = load_data()

# ---------------- ADD ENTRY ----------------
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

        latest_df = load_data()

        new_id = 1 if latest_df.empty else latest_df["id"].max() + 1

        new_entry = pd.DataFrame([{
            "id": new_id,
            "date": str(date),
            "type": entry_type,
            "category": category.title(),
            "amount": float(amount),
            "description": description
        }])

        updated_df = pd.concat([latest_df, new_entry], ignore_index=True)

        save_data(updated_df)

        st.sidebar.success("Entry Added Successfully!")
        st.rerun()

    else:
        st.sidebar.error("Please enter valid details.")


# Reload updated data
df = load_data()

# Convert types safely
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# ---------------- SHOW DATA ----------------
st.subheader("All Transactions")
st.dataframe(df.sort_values("date", ascending=False))


# ---------------- DELETE ENTRY ----------------
st.subheader("Delete Entry")

if not df.empty:

    delete_id = st.selectbox(
        "Select Transaction ID to Delete",
        df["id"].tolist()
    )

    if st.button("Delete Selected Entry"):
        updated_df = df[df["id"] != delete_id]
        save_data(updated_df)

        st.success(f"Entry with ID {delete_id} deleted successfully!")
        st.rerun()


# ---------------- SUMMARY ----------------
if not df.empty:

    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    savings = total_income - total_expense

    st.subheader("Overall Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rs. {total_income:.2f}")
    col2.metric("Total Expense", f"Rs. {total_expense:.2f}")
    col3.metric("Total Savings", f"Rs. {savings:.2f}")


# ---------------- MONTHLY ANALYSIS ----------------
st.subheader("📅 Monthly Analysis")

if not df.empty:

    df["year_month"] = df["date"].dt.to_period("M")

    months = sorted(df["year_month"].astype(str).dropna().unique())

    if months:
        selected_month = st.selectbox("Select Month", months)

        filtered_df = df[df["year_month"].astype(str) == selected_month]

        month_income = filtered_df[filtered_df["type"] == "Income"]["amount"].sum()
        month_expense = filtered_df[filtered_df["type"] == "Expense"]["amount"].sum()
        month_savings = month_income - month_expense

        st.write(f"### Income: Rs. {month_income:.2f}")
        st.write(f"### Expense: Rs. {month_expense:.2f}")
        st.write(f"### Savings: Rs. {month_savings:.2f}")

        expense_data = filtered_df[filtered_df["type"] == "Expense"]

        if not expense_data.empty:
            category_summary = expense_data.groupby("category")["amount"].sum()
            st.write("### Category-wise Expense (Bar Chart)")
            st.bar_chart(category_summary)
        else:
            st.info("No expenses for selected month.")