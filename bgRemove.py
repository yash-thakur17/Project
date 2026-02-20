import streamlit as st
import os
from PIL import Image
from rembg import remove
from io import BytesIO

st.title("AI Background Remover")

upload_file = st.file_uploader("Upload an image to remove the background", type=["png", "jpg", "jpeg"])

if upload_file:
    img = Image.open(upload_file)

    st.subheader("Original Image")
    st.image(img, use_column_width=True)

    if st.button("Remove Background"):
        with st.spinner("Removing Background..."):
            output = remove(img)

        st.subheader("Image with Removed Background")
        st.image(output)

        img_bytes = BytesIO()
        output.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        st.download_button(
            label="Download Image",
            data=img_bytes,
            file_name="removed_background.png",
            mime="image/png"
        )
