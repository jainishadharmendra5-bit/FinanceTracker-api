import streamlit as st
import requests
import pandas as pd

API_URL = "https://finance-api-isip.onrender.com"

st.set_page_config(
    page_title="Finance Tracker",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Finance Tracker Dashboard")
st.caption("Track income, expenses, and financial insights")

def load_data():
    res = requests.get(f"{API_URL}/transactions")
    return res.json() if res.status_code == 200 else []

data = load_data()
df = pd.DataFrame(data) if data else pd.DataFrame(columns=["id","category","amount","type"])

st.sidebar.header("➕ Add / Edit Transaction")

edit_mode = st.sidebar.checkbox("Edit existing transaction")

with st.sidebar.form("form"):
    tid = st.number_input("ID (only for edit)", min_value=0, step=1)
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    ttype = st.selectbox("Type", ["income", "expense"])
    submit = st.form_submit_button("Submit")

if submit:
    try:
        payload = {
            "category": category,
            "amount": amount,
            "type": ttype
        }

        if edit_mode:
            res = requests.put(f"{API_URL}/transactions/{int(tid)}", json=payload)
        else:
            res = requests.post(f"{API_URL}/transactions", json=payload)

        if res.status_code == 200:
            st.sidebar.success("Success!")
            st.rerun()
        else:
            st.sidebar.error("Request failed")
    except Exception as e:
        st.sidebar.error(e)

st.subheader("📊 Overview")

income = df[df["type"] == "income"]["amount"].sum()
expense = df[df["type"] == "expense"]["amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("Income", f"£{income}")
col2.metric("Expense", f"£{expense}")
col3.metric("Balance", f"£{balance}")

st.divider()

col4, col5 = st.columns(2)

with col4:
    st.subheader("Income vs Expense")
    if not df.empty:
        st.bar_chart(df.groupby("type")["amount"].sum())

with col5:
    st.subheader(" Category Breakdown")
    if not df.empty:
        st.bar_chart(df.groupby("category")["amount"].sum())


st.subheader("🧾 Transactions")

if df.empty:
    st.info("No transactions yet")
else:
    for _, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

        col1.write(row["id"])
        col2.write(row["category"])
        col3.write(row["amount"])
        col4.write(row["type"])

        if col5.button("🗑️ Delete", key=f"del_{row['id']}"):
            requests.delete(f"{API_URL}/transactions/{row['id']}")
            st.rerun()


st.divider()

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    data=csv,
    file_name="transactions.csv",
    mime="text/csv"
)


if st.button("🔄 Refresh"):
    st.rerun()

 