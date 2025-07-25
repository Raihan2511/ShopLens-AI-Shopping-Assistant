import streamlit as st
from app.config import settings
from app.services import get_text_based_rec, get_image_based_rec
from app.services.chat import load_chat_history, save_chat_message
from app.components.chat import render_chat_bubble, render_category_selection
from app.services.ai import infer_query
from PIL import Image
import requests
from io import BytesIO
from app.services.image_processing import get_detections

# Set up page
st.set_page_config(page_title="ShopLens", layout="wide")
st.title("💬 ShopLens AI Stylist")

# Spacer to push the button to bottom
sidebar_space = st.sidebar.container()
for _ in range(300):  # Fills space dynamically; tweak if needed
    sidebar_space.empty()

# Button fixed at bottom
with st.sidebar:
    if st.button("📤 Upload Image"):
        st.session_state.uploader_visible = True

cats = ['shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan', 'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit', 'cape', 'glasses', 'hat', 'headband, head covering, hair accessory', 'tie', 'glove', 'watch', 'belt', 'leg warmer', 'tights, stockings', 'sock', 'shoe', 'bag, wallet', 'scarf', 'umbrella', 'hood', 'collar', 'lapel', 'epaulette', 'sleeve', 'pocket', 'neckline', 'buckle', 'zipper', 'applique', 'bead', 'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel']

# Load chat from session or DB
if "chat" not in st.session_state:
    st.session_state.chat = load_chat_history()

if "uploader_visible" not in st.session_state:
    st.session_state.uploader_visible = False

if "image" not in st.session_state:
    st.session_state.image = None

if "image_query" not in st.session_state:
    st.session_state.image_query = None

if "clicked_cat" not in st.session_state:
    st.session_state.clicked_cat = None

def show_upload(state:bool):
    st.session_state.uploader_visible = state

prompt = st.chat_input("What outfit are you looking for?")


inferred_query = infer_query(prompt) if prompt else None

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
            st.session_state.image_query = prompt
            if not st.session_state.uploader_visible:
                show_upload(True)
        else:
            st.session_state.image_query = prompt
            url = inferred_query["image_url"]  # example: "https://example.com/image.jpg"
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            product_ids = get_image_based_rec(img)

            save_chat_message(prompt, product_ids)

            st.session_state.chat.append({
            "role": "user",
            "content": f"",
            "image": img,
        })

            st.session_state.chat.append({
                "role": "assistant",
                "content": f"Here's my recommendations:",
                "product_ids": product_ids
            })

# Render chat
for msg in st.session_state.chat:
    render_chat_bubble(msg)

if st.session_state.uploader_visible:
    st.session_state.image = st.file_uploader("", type=["png", "jpg", "jpeg"])
    if st.session_state.image:
        show_upload(False)
        image = Image.open(st.session_state.image)

        st.session_state.chat.append({
            "role": "user",
            "content": f"Showing products similar to this image:",
            "image": st.session_state.image,
        })

        image, boxes, labels = get_detections(image)

        render_category_selection(image, boxes, labels)


if st.session_state.clicked_cat:
    product_ids = get_image_based_rec(st.session_state.clicked_cat["image"])

    # save_chat_message(st.session_state.image_query, product_ids)

    st.session_state.chat.append({
        "role": "assistant",
        "content": f"Showing cropped image:",
        "image": st.session_state.clicked_cat["image"],
    })

    st.session_state.chat.append({
        "role": "assistant",
        "content": f"Here's my recommendations:",
        "product_ids": product_ids
    })

    st.session_state.clicked_cat = None
    # Reset the clicked category to None to avoid re-rendering
    st.rerun()


# Debug info
if settings.DEBUG:
    st.sidebar.markdown("🔧 **Debug Info**")
    st.sidebar.write("DB URL:", settings.DB_URL)
    st.sidebar.write("Mode: DEBUG")
