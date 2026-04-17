from google import genai
from dotenv import load_dotenv
import os
import io
import streamlit as st
from gtts import gTTS


load_dotenv()
api_key = os.getenv("GEMENI_API")

client = genai.Client(api_key=api_key)


# not generate
def not_generator(images):
    promted = """Summarize the picture in note format at max 100 wogit, 
    make sure to necessary markdown to differentiate section and give me ans bangla language"""
    res = client.models.generate_content(
        model="gemini-3-flash-preview", contents=[images, promted]
    )
    return res.text


def audio_speech(text):
    speech = gTTS(text, lang="bn", slow=False)

    # speech.save("wellcome.mp3")
    audio_buff = io.BytesIO()
    speech.write_to_fp(audio_buff)
    return audio_buff


def quize_generate(images, defficulty):
    promted = f"""Use language bangla and  Analyze the uploaded image and identify the important concepts.

    Based on those concepts, generate a quiz with {defficulty} difficulty level.

    Rules:
    - Generate 5 questions.
    - Each question must have 4 options (A, B, C, D).
    - Highlight the correct answer.
    - Focus only on the important information from the image.

    Format the output using Markdown.

    ## Format

    ### Question 1
    A.  
    B.  
    C.  
    D.  

    **Answer:** 
    """
    res = client.models.generate_content(
        model="gemini-3-flash-preview", contents=[images, promted]
    )
    return res.text
