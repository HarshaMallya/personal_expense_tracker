import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from db import create_db, add_expense, get_expenses, delete_expense, update_expense

# Initialize database
create_db()

# Streamlit Page Configuration
st.set_page_config(page_title="💰 Expense Tracker Dashboard", layout="wide")
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💰 Personal Expense Tracker Dashboard")

# Tabs for sections
tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📋 Manage Expenses", "📈 Analytics"])

# ---------------- TAB 1: ADD EXPENSE ----------------
with tab1:
    st.subheader("➕ Add a New Expense")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"])
    with col3:
        description = st.text_input("Description")
    with col4:
        date = st.date_input("Date", datetime.today())

    if st.button("💾 Add Expense"):
        add_expense(amount, category, description, str(date))
        st.success(f"✅ Added ₹{amount} under {category}")

# ---------------- TAB 2: MANAGE EXPENSES ----------------
with tab2:
    st.subheader("📋 Manage Expenses")
    expenses = get_expenses()

    if not expenses.empty:
        st.dataframe(expenses, use_container_width=True)

        selected_id = st.selectbox("Select ID to Edit/Delete", expenses["id"])
        record = expenses[expenses["id"] == selected_id].iloc[0]

        e_amount = st.number_input("Edit Amount", value=float(record["amount"]))
        e_category = st.selectbox("Edit Category",
                                  ["Food", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"],
                                  index=["Food", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"].index(record["category"]))
        e_description = st.text_input("Edit Description", value=record["description"])
        e_date = st.date_input("Edit Date", value=pd.to_datetime(record["date"]).date())

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✏️ Update"):
                update_expense(selected_id, e_amount, e_category, e_description, str(e_date))
                st.success("Record Updated ✅")
        with c2:
            if st.button("🗑️ Delete"):
                delete_expense(selected_id)
                st.warning("Record Deleted ⚠️")
    else:
        st.info("No records found. Add expenses first!")

# ---------------- TAB 3: ANALYTICS ----------------
with tab3:
    st.subheader("📊 Expense Analytics")

    df = get_expenses()
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Total Spent", f"₹{df['amount'].sum():,.2f}")
        col2.metric("📅 Average Expense", f"₹{df['amount'].mean():,.2f}")
        top_cat = df.groupby("category")["amount"].sum().idxmax()
        col3.metric("🏆 Top Category", top_cat)

        # Charts
        st.markdown("---")
        col4, col5 = st.columns(2)

        with col4:
            st.write("### 🥧 Expense by Category")
            fig1, ax1 = plt.subplots()
            category_summary = df.groupby("category")["amount"].sum()
            ax1.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%", startangle=90)
            st.pyplot(fig1)

        with col5:
            st.write("### 📅 Monthly Spending Trend")
            df["month"] = df["date"].dt.to_period("M")
            monthly_summary = df.groupby("month")["amount"].sum()
            fig2, ax2 = plt.subplots()
            sns.lineplot(x=monthly_summary.index.astype(str), y=monthly_summary.values, marker="o", color="#ff6600", ax=ax2)
            ax2.set_xlabel("Month")
            ax2.set_ylabel("Total Spent (₹)")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
    else:
        st.info("No data available for analytics.")
