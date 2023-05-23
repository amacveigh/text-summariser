import openai
import streamlit as st
import sys
sys.path.append('/path/to/ffmpeg')
import os
import numpy as np
import tempfile
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

def transcribe_on_web(audio_file):
    with open(audio_file.name,'wb') as f:
         f.write(audio_file.getbuffer())

    open_path = open(audio_file.name, "rb")
        # print("opened")
    transcript = openai.Audio.transcribe("whisper-1", open_path)

    st.session_state["transcribe"] = transcript.text

def translate(prompt):
    try:
        st.session_state["transcribe"] = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
            {"role": "user", "content": f"Please translate the following text into English {prompt}"}],
            max_tokens=700,
            temperature=0.1,
        )["choices"][0]["message"]["content"]
        
    except:
        st.write('There was an error =(')
        

def summarize_turbo(prompt):
    augmented_prompt = [{"role": "user", "content": f"""Based on the provided text below, generate a short summary. Also give bullet points covering the main themes of the text.

       Text: ###
       {prompt}
       ###
       """}]
    try:
        st.session_state["summary"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=.7,
            max_tokens=700,
        )["choices"][0]["message"]["content"]
    except:
        st.write('There was an error =(')

def gen_article(prompt):
    augmented_prompt = [{"role": "user", "content": f"""Based on the provided text below, generate an article with a catchy headline, intorduction summarizing the main points, and several paragraphs.

       Text: ###
       {prompt}
       ###
       """}]
    try:
        st.session_state["gen_article"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=.7,
            max_tokens=1000,
        )["choices"][0]["message"]["content"]
    except:
        st.write('There was an error =(')

def gen_article_wireless(prompt):
    augmented_prompt = [{"role": "user", "content": f"""
    From the Text below generate an article with the following:
    1. A catchy headline .
    2. A word count 500 and 600 words.
    3. An introduction summarizing the main points
    4. A sentence with a quote from the Text
    5. A sub heading and paragraph at the bottom evaluating the emotion in the text

    Text: ###
    {prompt}
    ###
    """}]
    try:
        st.session_state["gen_article_wireless"] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=augmented_prompt,
            temperature=1,
            max_tokens=2000,
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
            max_tokens=700,
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