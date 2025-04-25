import streamlit as st
import os
from PIL import Image

def render_product_card(product, show_details=True):
    col1, col2 = st.columns([1, 2])
    with col1:
      with st.container(height=175, border=None):
        if os.path.exists(product.image_url):
            st.image(Image.open(product.image_url), width=150)
        else:
            st.image("https://via.placeholder.com/150", caption="Image not found", width=150)
    with col2:
        st.markdown(f"### {product.title}")
        st.markdown(f"**₹{int(product.price)}**")
        if show_details:
          with st.expander("Description"):
            st.write(product.description)
        st.button("Add to Cart", key=f"cart_{product.id}", on_click=lambda: None)
