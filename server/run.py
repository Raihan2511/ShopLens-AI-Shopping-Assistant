import streamlit as st
from app.config import settings

st.set_page_config(page_title="ShopLens", layout="wide")

# Title
st.title("🛍️ Welcome to ShopLens")

# Description
st.markdown("""
Welcome to **ShopLens**, your one-stop fashion e-commerce platform.

Use the sidebar to:
- 🛒 Browse products
- 💬 Chat with our AI stylist
- 📦 View your orders
- 👤 Manage your account
""")

# Show debug info
if settings.DEBUG:
    st.sidebar.markdown("🔧 **Debug Info**")
    st.sidebar.write("DB URL:", settings.DB_URL)
    st.sidebar.write("Mode: DEBUG")

st.success("Use the sidebar to navigate.")
