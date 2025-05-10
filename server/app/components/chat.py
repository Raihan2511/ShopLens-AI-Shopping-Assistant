import streamlit as st
from app.utils.helpers import fetch_products_by_ids
from app.components import render_product_card
import math

cats = ['shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan', 'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit', 'cape', 'glasses', 'hat', 'headband, head covering, hair accessory', 'tie', 'glove', 'watch', 'belt', 'leg warmer', 'tights, stockings', 'sock', 'shoe', 'bag, wallet', 'scarf', 'umbrella', 'hood', 'collar', 'lapel', 'epaulette', 'sleeve', 'pocket', 'neckline', 'buckle', 'zipper', 'applique', 'bead', 'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel']

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

def render_category_selection(image, boxes, labels):
    seen = set()
    cat_labels = []

    for label, box in zip(labels, boxes):
        cat_name = cats[label]
        if cat_name and cat_name not in seen:
            seen.add(cat_name)
            xmin, ymin, xmax, ymax = box.int().tolist()
            cropped = image.crop((xmin, ymin, xmax, ymax))
            cat_labels.append((label, cat_name, cropped))

    MAX_COLS = 6
    ROW_HEIGHT = 175
    total = len(cat_labels)
    num_rows = math.ceil(total / MAX_COLS)

    for row_idx in range(num_rows):
        cols = st.columns(MAX_COLS)
        for i in range(MAX_COLS):
            idx = row_idx * MAX_COLS + i
            if idx < total:
                label, cat_name, cropped = cat_labels[idx]
                with cols[i]:
                    with st.container(height=ROW_HEIGHT, border=None):
                        st.image(cropped, use_container_width=True)
                    st.button(
                        cat_name,
                        key=f"{cat_name}_{row_idx}_{i}",
                        use_container_width=True,
                        on_click=lambda label=label, cat_name=cat_name, cropped=cropped: handle_category_click(label, cat_name, cropped)
                    )
            else:
                cols[i].empty()


def handle_category_click(label, cat_name, cropped):
    st.session_state.clicked_cat = {
        "label": label,
        "name": cat_name,
        "image": cropped,
    }