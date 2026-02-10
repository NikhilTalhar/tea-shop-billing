import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Tea Shop Billing", layout="wide")

# ---------------- SESSION STATE ----------------
if "menu" not in st.session_state:
    st.session_state.menu = {
        "Tea": 10,
        "Half Tea": 7,
        "Coffee": 15,
        "Idli Chutney": 25,
        "Idli Sambar": 30
    }

if "current_order" not in st.session_state:
    st.session_state.current_order = []

if "all_orders" not in st.session_state:
    st.session_state.all_orders = []

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* Background */
.main {
    background-color: #f5f5f5;
}

/* Big Square Buttons */
div.stButton > button {
    height: 120px;
    width: 120px;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    background-color: #1f1f1f;
    color: white;
    border: 2px solid #f8b400;
    margin: 8px;
    transition: 0.2s ease-in-out;
}

div.stButton > button:hover {
    background-color: #f8b400;
    color: black;
    transform: scale(1.05);
}

/* Total Styling */
.total-box {
    background-color: #1f1f1f;
    color: #f8b400;
    padding: 15px;
    border-radius: 10px;
    font-size: 22px;
    text-align: center;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("☕ Tea Shop POS Billing System")

# ---------------- MENU MANAGEMENT ----------------
with st.expander("⚙ Manage Menu"):
    col1, col2 = st.columns(2)

    with col1:
        new_item = st.text_input("New Item Name")
    with col2:
        new_price = st.number_input("Price", min_value=0, step=1)

    if st.button("Add Item"):
        if new_item:
            st.session_state.menu[new_item] = new_price
            st.success("Item Added")

    st.markdown("### Edit Prices")

    for item in list(st.session_state.menu.keys()):
        updated_price = st.number_input(
            f"{item}",
            value=st.session_state.menu[item],
            key=f"price_{item}"
        )
        st.session_state.menu[item] = updated_price

st.divider()

# ---------------- BILLING SECTION ----------------
st.subheader("🧾 Create Order")

cols = st.columns(4)

i = 0
for item, price in st.session_state.menu.items():
    if cols[i % 4].button(f"{item}\n₹{price}", key=f"btn_{item}"):
        st.session_state.current_order.append((item, price))
    i += 1

st.markdown("### Current Order")

total = 0
for item, price in st.session_state.current_order:
    st.write(f"{item} - ₹{price}")
    total += price

st.markdown(f'<div class="total-box">Total: ₹{total}</div>', unsafe_allow_html=True)

colA, colB = st.columns(2)

with colA:
    if st.button("✅ Complete Order"):
        if st.session_state.current_order:
            timestamp = datetime.now()
            for item, price in st.session_state.current_order:
                st.session_state.all_orders.append({
                    "Date": timestamp.date(),
                    "Time": timestamp.strftime("%H:%M:%S"),
                    "Item": item,
                    "Price": price
                })
            st.session_state.current_order = []
            st.success("Order Saved")

with colB:
    if st.button("❌ Clear Current Order"):
        st.session_state.current_order = []

st.divider()

# ---------------- END OF DAY REPORT ----------------
st.subheader("📊 End of Day Report")

if st.session_state.all_orders:
    df = pd.DataFrame(st.session_state.all_orders)

    total_sales = df["Price"].sum()
    st.markdown(f'<div class="total-box">Total Sales Today: ₹{total_sales}</div>', unsafe_allow_html=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name="daily_sales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No sales recorded today.")
