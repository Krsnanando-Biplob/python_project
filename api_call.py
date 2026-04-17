from google import genai
from dotenv import load_dotenv
import os
import io
from gtts import gTTS

load_dotenv()

api_key = os.getenv("GENERATE_API")  # FIXED

client = genai.Client(api_key=api_key)


# ================= NOTE GENERATOR =================
def not_generator(images):
    prompt = """Summarize the picture in note format at max 100 words,
    use necessary markdown to separate sections and give answer in Bangla language."""

    res = client.models.generate_content(
        model="gemini-1.5-flash",   # FIXED MODEL
        contents=[prompt] + images   # FIXED INPUT ORDER
    )

    return res.text


# ================= AUDIO =================
def audio_speech(text):
    if not text:
        return None

    speech = gTTS(text, lang="bn", slow=False)

    audio_buff = io.BytesIO()
    speech.write_to_fp(audio_buff)
    audio_buff.seek(0)   # IMPORTANT FIX

    return audio_buff


# ================= QUIZ GENERATOR =================
def quize_generate(images, difficulty):
    prompt = f"""Use Bangla language and analyze the uploaded image.

Generate a quiz with {difficulty} difficulty.

Rules:
- 5 questions
- Each question has 4 options (A, B, C, D)
- Highlight correct answer
- Focus only on image content

Format:

### Question 1
A.
B.
C.
D.

**Answer:**"""

    res = client.models.generate_content(
        model="gemini-1.5-flash",   # FIXED MODEL
        contents=[prompt] + images
    )

    return res.text