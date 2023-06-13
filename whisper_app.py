import streamlit as st
st.set_page_config(layout="wide")

import openai
import os
from text_summarizer.functions import headline
from text_summarizer.functions import summarize_turbo
from text_summarizer.functions import gen_article_wireless
from text_summarizer.functions import transcribe_on_web
from text_summarizer.functions import SEO
from text_summarizer.functions import translate
from text_summarizer.functions import gen_article
from text_summarizer.functions import transcribe_force_eng
from text_summarizer.functions import americanize
# from text_summarizer import americanisms
import json
# import whisper
f = open('text_summarizer/americanisms.json')
# returns JSON object as 
# a dictionary
americanisms = json.load(f)

try:
  openai.api_key = os.getenv('OPENAI_TURBO_KEY')
  
  if "summary" not in st.session_state:
      st.session_state["summary"] = ""

  if "americanize" not in st.session_state:
      st.session_state["americanize"] = ""

  if "transcribe" not in st.session_state:
      st.session_state["transcribe"] = ""

  if "title" not in st.session_state:
      st.session_state["title"] = ""
  
  if "gen_article" not in st.session_state:
      st.session_state["gen_article"] = ""

  if "seo" not in st.session_state:
      st.session_state["seo"] = ""

  if "translate" not in st.session_state:
      st.session_state["translate"] = ""

  if "gen_article_wireless" not in st.session_state:
      st.session_state["gen_article_wireless"] = ""
  
  st.title("AI Audio Pipeline")
  
  audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a","mp4"])
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
      on_click=transcribe_on_web,
      kwargs={"audio_file": audio_file},
  )

  st.button(
      "Transcribe Force English",
      on_click=transcribe_force_eng,
      kwargs={"audio_file": audio_file},
  )



  input_text = st.text_area(label="Enter full text:", value=st.session_state["transcribe"], height=250)
  
  st.button(
      "Convert to American English",
      on_click=americanize,
      kwargs={"string": input_text, "word_list": americanisms},
  )

  st.button(
      "Summarise",
      on_click=summarize_turbo,
      kwargs={"prompt": input_text},
  )

  st.button(
      "Translate",
      on_click=translate,
      kwargs={"prompt": input_text},
  )

  output_text = st.text_area(label="Summarized text:", value=st.session_state["summary"], height=250)

  key_words = st.text_input(label="Headline Tailoring:", value="EG: 'Be lighthearted/funny/serious' , 'Use the word ____' , 'Use alliteration.'", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, label_visibility="visible")

  st.button(
      "Generate Suggested Titles",
      on_click=headline,
      kwargs={"prompt": input_text, "key_words": key_words},
  )
  title_text = st.text_area(label="Title:", value=st.session_state["title"], height=150)

  st.button(
      "Generate Article Example",
      on_click=gen_article,
      kwargs={"prompt": input_text},
  )
  article_text = st.text_area(label="Article Generation", value=st.session_state["gen_article"], height=350)

  st.button(
      "Generate SEO Tags",
      on_click=SEO,
      kwargs={"prompt": input_text},
  )
  seo_text = st.text_area(label="SEO Tags:", value=st.session_state["seo"], height=150)

  st.button(
      "Broadcast Article",
      on_click=gen_article_wireless,
      kwargs={"prompt": input_text},
  )
  wireless = st.text_area(label="Broadcast Article : 350-600 words, highlighted quote, emotion evaluation", value=st.session_state["gen_article_wireless"], height=500)
  

#   americanized = st.text_area(label="UK to US Localisation", value=st.session_state["americanize"], height=500)



except:
  st.write('There was an error =(')