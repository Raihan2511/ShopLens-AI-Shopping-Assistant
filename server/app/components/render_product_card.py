import streamlit as st
import os
from PIL import Image
import uuid

def render_product_card(product, show_details=True):
    col1, col2 = st.columns([1, 2])
    with col1:
      with st.container(height=175, border=None):
        if os.path.exists(product.image_url):
            st.image(Image.open(product.image_url), width=150)
        else:
            st.image("https://via.placeholder.com/150", caption="Image not found", width=150)
    with col2:
        title = product.title
        min_title_len = 30
        if len(title) < min_title_len:
            title = title + "‎ " * (min_title_len - len(title))
        st.markdown(f"### {title}")
        st.markdown(f"**₹{int(product.price)}**")
        if show_details:
          with st.expander("Description"):
            st.write(product.description)
        unique_key = f"cart_{product.id}_{uuid.uuid4().hex}"
        st.button("Add to Cart", key=unique_key, on_click=lambda: None)