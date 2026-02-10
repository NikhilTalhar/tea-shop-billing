import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Tea Shop Billing", layout="wide")

# Initialize session states
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

st.title("☕ Tea Shop Billing System")

# -----------------------
# MENU MANAGEMENT
# -----------------------
st.subheader("Manage Menu")

col1, col2 = st.columns(2)

with col1:
    new_item = st.text_input("Add New Item")
with col2:
    new_price = st.number_input("Price", min_value=0)

if st.button("Add Item"):
    if new_item:
        st.session_state.menu[new_item] = new_price
        st.success("Item Added")

st.write("### Edit Prices")

for item in list(st.session_state.menu.keys()):
    new_price = st.number_input(
        f"{item} Price",
        value=st.session_state.menu[item],
        key=item
    )
    st.session_state.menu[item] = new_price

st.divider()

# -----------------------
# BILLING SECTION
# -----------------------
st.subheader("Create Order")

cols = st.columns(3)

i = 0
for item, price in st.session_state.menu.items():
    if cols[i % 3].button(f"{item}\n₹{price}"):
        st.session_state.current_order.append((item, price))
    i += 1

st.write("### Current Order")

total = 0
for item, price in st.session_state.current_order:
    st.write(f"{item} - ₹{price}")
    total += price

st.write(f"## Total: ₹{total}")

if st.button("Complete Order"):
    if st.session_state.current_order:
        timestamp = datetime.now()
        for item, price in st.session_state.current_order:
            st.session_state.all_orders.append({
                "Date": timestamp.date(),
                "Time": timestamp.time(),
                "Item": item,
                "Price": price
            })
        st.session_state.current_order = []
        st.success("Order Saved")

if st.button("Clear Current Order"):
    st.session_state.current_order = []

st.divider()

# -----------------------
# DOWNLOAD EXCEL
# -----------------------
st.subheader("End of Day Report")

if st.session_state.all_orders:
    df = pd.DataFrame(st.session_state.all_orders)

    total_sales = df["Price"].sum()
    st.write(f"### Total Sales Today: ₹{total_sales}")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="Download Excel Report",
        data=output.getvalue(),
        file_name="daily_sales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No sales yet today.")
