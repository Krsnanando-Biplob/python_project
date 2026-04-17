import streamlit as st
from api_call import not_generator, audio_speech, quize_generate
from PIL import Image

st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()

with st.sidebar:
    st.header("Controls")

    images = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    pil_images = []

    if images:
        if len(images) > 3:
            st.error("Upload at max 3 images")
            st.stop()

        for img in images:
            pil_img = Image.open(img)
            pil_images.append(pil_img)

        st.subheader("Your uploaded images")
        cols = st.columns(len(images))

        for i, img in enumerate(images):
            with cols[i]:
                st.image(img)

    selected_option = st.selectbox(
        "Enter Difficulty",
        ("Easy", "Medium", "Hard"),
        index=None
    )

    pressed = st.button("Click And Generate", type="primary")

# ================= MAIN =================

if pressed:

    if not images:
        st.error("You must upload one image")

    elif not selected_option:
        st.error("You must select a difficulty")

    else:

        # NOTE
        with st.container(border=True):
            st.subheader("Note")

            with st.spinner("AI is writing notes..."):
                generated_note = not_generator(pil_images)
                st.markdown(generated_note)

        # AUDIO
        with st.container(border=True):
            st.subheader("Audio")

            with st.spinner("Creating Audio..."):
                clean_text = generated_note

                for char in ["#", "$", "-", "_", "'", "!", ",", "*"]:
                    clean_text = clean_text.replace(char, "")

                audio_file = audio_speech(clean_text)
                st.audio(audio_file)

        # QUIZ
        with st.container(border=True):
            st.subheader(f"Quiz Level ({selected_option})")

            with st.spinner("AI is generating quiz..."):
                quiz = quize_generate(pil_images, selected_option)
                st.markdown(quiz)