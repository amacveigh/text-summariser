import openai
import streamlit as st

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

        

def transcribe(audio_file):
    read = audio_file.read()
    file = open(read, "rb")
    try:
        text = openai.Audio.transcribe("whisper-1", file).text
        print(text)
        st.session_state["transcribe"] = text
        print(text)
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