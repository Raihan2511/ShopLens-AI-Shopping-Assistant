import streamlit as st
from app.config import settings
from app.models import Product, Message
import json
from app.db.session import engine
from sqlalchemy.orm import Session
import os
from PIL import Image
from app.components import render_product_card
from app.services import get_text_based_rec
from app.services.chat import load_chat_history, save_chat_message
from app.components.chat import render_chat_bubble
from app.services.ai import infer_query
import time


# Set up page
st.set_page_config(page_title="ShopLens", layout="wide")
st.title("💬 ShopLens AI Stylist")

# Fetch mock recommended products (replace with actual logic)
def get_recommended_products(query):
    product_ids = get_text_based_rec(query)
    with Session(bind=engine) as session:
        return session.query(Product).where(Product.id.in_(product_ids)).all()

# Load chat from session or DB
if "chat" not in st.session_state:
    st.session_state.chat = load_chat_history()

if "uploader_visible" not in st.session_state:
    st.session_state.uploader_visible = False

def show_upload(state:bool):
    st.session_state.uploader_visible = state

# Main chat area
prompt = st.chat_input("What outfit are you looking for?")

inferred_query = infer_query(prompt) if prompt else None
print(type(inferred_query))
print(inferred_query)

if inferred_query:
    st.session_state.chat.append({"role": "user", "content": prompt})

    if inferred_query["query_type"] == "text based product search":
        product_ids = get_text_based_rec(inferred_query["search_term"], k=inferred_query["no_of_results"])
        save_chat_message(prompt, product_ids)

        st.session_state.chat.append({
            "role": "assistant",
            "content": f"Here's my recommendations:",
            "product_ids": product_ids
        })

    elif inferred_query["query_type"] == "image based product search":
        if inferred_query["image_url"] is None:
            if not st.session_state["uploader_visible"]:
                show_upload(True)

# Render chat
for msg in st.session_state.chat:
    render_chat_bubble(msg)

if st.session_state.uploader_visible:
    st.session_state.file = st.file_uploader("")
    if st.session_state.file:
        with st.spinner("Processing your image..."):
            time.sleep(5)
    show_upload(False)

# Debug info
if settings.DEBUG:
    st.sidebar.markdown("🔧 **Debug Info**")
    st.sidebar.write("DB URL:", settings.DB_URL)
    st.sidebar.write("Mode: DEBUG")
