import streamlit as st
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models import Product
from app.db.base import Base
from app.components import render_product_card

PAGE_SIZE = 12  # Number of products to load per click

def get_products(offset=0, limit=PAGE_SIZE):
    with Session(bind=engine) as session:
        return session.query(Product).offset(offset).limit(limit).all()

def render_product(product):
    render_product_card(product)

def show_product_grid():
    st.title("🛍️ ShopLens — Browse Products")

    if "product_offset" not in st.session_state:
        st.session_state.product_offset = 0
    if "loaded_products" not in st.session_state:
        st.session_state.loaded_products = []

    # If "load_more_triggered" flag is set, load more products
    if st.session_state.get("load_more_triggered", False):
        new_products = get_products(offset=st.session_state.product_offset)
        if new_products:
            st.session_state.loaded_products.extend(new_products)
            st.session_state.product_offset += PAGE_SIZE
        else:
            st.warning("No more products to load.")
        st.session_state.load_more_triggered = False  # Reset flag

    # Render all loaded products
    products = st.session_state.loaded_products
    for i in range(0, len(products), 3):
        row = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                with row[j]:
                    render_product(products[i + j])

    # Button only sets flag
    if st.button("🔄 Load More"):
        st.session_state.load_more_triggered = True

# Entry point
if __name__ == "__main__":
    st.set_page_config(page_title="ShopLens | Products", layout="wide")
    show_product_grid()
