import streamlit as st
from app.config import settings
from app.models import Product
from app.db.session import engine
from sqlalchemy.orm import Session
import os
from PIL import Image
from app.components import render_product_card
from app.services import get_text_based_rec

# Set up page
st.set_page_config(page_title="ShopLens", layout="wide")
st.title("💬 ShopLens AI Stylist")

# Chat history using session_state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Fetch mock recommended products (replace with actual logic)
def get_recommended_products(query):
    product_ids = get_text_based_rec(query)
    with Session(bind=engine) as session:
        return session.query(Product).where(Product.id.in_(product_ids)).all()

# Reusable product card
def render_product(product):
    with st.container():
        render_product_card(product, show_details=False)

# Main chat area
prompt = st.chat_input("What outfit are you looking for?")
if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    # Dummy response – replace with your recommendation logic or LLM integration
    response_text = f"Here's what I recommend for: **{prompt}**"
    st.session_state.chat.append({"role": "assistant", "content": response_text})

# Render chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            # Render product recommendations under assistant messages
            products = get_recommended_products(msg["content"])
            cols = st.columns(3)
            for i, product in enumerate(products):
                with cols[i % 3]:
                    render_product(product)

# Debug info
if settings.DEBUG:
    st.sidebar.markdown("🔧 **Debug Info**")
    st.sidebar.write("DB URL:", settings.DB_URL)
    st.sidebar.write("Mode: DEBUG")
