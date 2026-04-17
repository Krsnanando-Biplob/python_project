import streamlit as st
from api_call import not_generator,audio_speech,quize_generate
from PIL import Image


st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()

with st.sidebar:
    st.header("controls")
    images = st.file_uploader(
        "Upload images", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    pil_images = []
    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)

    if images:
        if len(images) > 3:
            st.error("Upload at max 3 images")
        else:
            cols = st.columns(len(images))
            st.subheader("Your uploaded images")

            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)

    selected_option = st.selectbox(
        "Enter Difficulty", ("Easy", "Medium", "Hard"), index=None
    )
    # if selected_option:
    #     st.markdown(f"Your selected: **{selected_option}**")
    # # else:
    #     st.error("You must select a option")
    pressed = st.button("Click And Generated", type="primary")


if pressed:
    if not images:
        st.error("You must upload one image")
    if not selected_option:
        st.error("You must selecte a difficulty")

    if images and selected_option:
        # note
        with st.container(border=True):
            st.subheader("Note")
            with st.spinner("Ai is writing notes for you"):
                gerareated_note = not_generator(pil_images)
                st.markdown(gerareated_note)

        # audio
        with st.container(border=True):
            st.subheader("Audio")
            
            with st.spinner("Creating Audio"):
                gerareated_note = gerareated_note.replace("#","")
                gerareated_note = gerareated_note.replace("$","")
                gerareated_note = gerareated_note.replace("-","")
                gerareated_note = gerareated_note.replace("_","")
                gerareated_note = gerareated_note.replace("'","")
                gerareated_note = gerareated_note.replace("!","")
                gerareated_note = gerareated_note.replace(",","")
                gerareated_note = gerareated_note.replace("*","")
                audio_spaces = audio_speech(gerareated_note)
                st.audio(audio_spaces)

        # quize
        with st.container(border=True):
            st.subheader(f"Selection level ({selected_option})")
            
            with st.spinner("Ai is writing Quize for you"):
                quize_gen = quize_generate(pil_images, selected_option)
            
                st.markdown(quize_gen)