import streamlit as st
from app.utils.helpers import fetch_products_by_ids
from app.components import render_product_card

def render_chat_bubble(msg):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "user" and "image" in msg:
            st.image(msg["image"], width=150)
        if msg["role"] == "assistant" and "image" in msg:
            st.image(msg["image"], width=150)
        if msg["role"] == "assistant" and "product_ids" in msg:
            render_product_grid(msg["product_ids"])

def render_product_grid(product_ids):
    products = fetch_products_by_ids(product_ids)
    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            with st.container():
                render_product_card(product, show_details=False)
