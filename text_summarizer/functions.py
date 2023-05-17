import openai
import streamlit as st
from tempfile import NamedTemporaryFile
import tempfile
# import whisper
from pydub import AudioSegment
import pydub
# from pathlib import Path
import sys
sys.path.append('/path/to/ffmpeg')
import os
import io
import numpy as np
# from scipy.io import wavfile
import logging
log = logging.getLogger(__name__)

def handle_uploaded_audio_file(uploaded_file):
    a = pydub.AudioSegment.from_wav(uploaded_file)

    st.write(a.sample_width)

    samples = a.get_array_of_samples()
    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples.typecode).max
    st.write(fp_arr.shape)

    return fp_arr, 22050

def summarize(prompt):
    augmented_prompt = f"summarize this text: {prompt}"
    try:
        st.session_state["summary"] = openai.Completion.create(
            model="text-davinci-003",
            prompt=augmented_prompt,
            temperature=.5,
            max_tokens=1000,
        )["choices"][0]["text"]
    except:
        st.write('There was an error =(')

def save_file(sound_file):
    # save your sound file in the right folder by following the path
    with open(os.path.join('audio_files/', sound_file.name),'wb') as f:
         f.write(sound_file.getbuffer())
    return sound_file.name

def transcribe(audio_file):
    log.debug("doing something!")
    try:  
        save_file(audio_file)
        file_path = f'audio_files/{audio_file.name}'
        print(file_path)
        open_path = open(file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", open_path)
        print('done')
        # print(transcript.text)
        st.session_state["transcribe"] = transcript.text
    except:
        st.write('There was an error =(')
        

def summarize_turbo(prompt):
    augmented_prompt = [{"role": "user", "content": f"""You are an expert journalist. Based on the provided text below, generate a short summary.

       Text: ###
       {prompt}
       ###
       """}]
    try:
        st.session_state["summary"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=.7,
            max_tokens=400,
        )["choices"][0]["message"]["content"]
    except:
        st.write('There was an error =(')

def headline(prompt):
    augmented_prompt = [{"role": "user", "content": f"""You are an expert journalist. Based on the provided text below, generate 5 different SEO friendly titles for a news article.

       Text: ###
       {prompt}
       ###
       """}]
    try:
        st.session_state["title"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=.7,
            max_tokens=400,
        )["choices"][0]["message"]["content"]
    except:
        st.write('There was an error =(')

def SEO(prompt):
    augmented_prompt = [{"role": "user", "content": f"""You are an expert in SEO. Based on the provided text below, suggest 5 tags optimised for SEO trends.

       Text: ###
       {prompt}
       ###
       """}]
    try:
        st.session_state["seo"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=.7,
            max_tokens=400,
        )["choices"][0]["message"]["content"]
    except:
        st.write('There was an error =(')