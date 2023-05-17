import streamlit as st
st.set_page_config(layout="wide")

import openai
import os
from text_summarizer.functions import headline
from text_summarizer.functions import summarize_turbo
from text_summarizer.functions import transcribe
from text_summarizer.functions import SEO
# import whisper

try:
  openai.api_key = os.getenv('OPENAI_TURBO_KEY')
  
  if "summary" not in st.session_state:
      st.session_state["summary"] = ""

  if "transcribe" not in st.session_state:
      st.session_state["transcribe"] = ""

  if "title" not in st.session_state:
      st.session_state["title"] = ""

  if "seo" not in st.session_state:
      st.session_state["seo"] = ""
  
  st.title("AI Audio Pipeline")
  
  audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
#   model = whisper.load_model("base")

  if audio_file is not None:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    # transcript = model.transcribe(audio_file.name)
    # transcript = openai.Audio.transcribe("whisper-1", audio_bytes)
    # st.session_state["transcribe"] = transcript.text
    # print(transcript["text"])

  st.button(
      "Transcribe",
      on_click=transcribe,
      kwargs={"audio_file": audio_file},
  )

  input_text = st.text_area(label="Enter full text:", value=st.session_state["transcribe"], height=250)

  st.button(
      "Summarise",
      on_click=summarize_turbo,
      kwargs={"prompt": input_text},
  )
  output_text = st.text_area(label="Summarized text:", value=st.session_state["summary"], height=250)

  st.button(
      "Generate Suggested Titles",
      on_click=headline,
      kwargs={"prompt": input_text},
  )
  title_text = st.text_area(label="Title:", value=st.session_state["title"], height=150)

  st.button(
      "Generate SEO Tags",
      on_click=SEO,
      kwargs={"prompt": input_text},
  )
  seo_text = st.text_area(label="SEO Tags:", value=st.session_state["seo"], height=150)

except:
  st.write('There was an error =(')