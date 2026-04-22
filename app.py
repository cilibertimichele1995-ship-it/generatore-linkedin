import streamlit as st
from groq import Groq
import os

# Inizializza client Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

st.title("✍️ LinkedIn post generator")

st.write("Enter your raw text and transform it into a LinkedIn post.")

# Input utente
user_input = st.text_area("Starting test", height=300)

tone = st.selectbox(
    "choose the post tone",
    ["Professional", "Ispirational"]
)

if st.button("Generate Post"):
    if not user_input.strip():
        st.warning("Please enter some text before generating.")
    else:
        with st.spinner("Generation in progress..."):

            prompt = f"""
            Trasforma il seguente testo in un post LinkedIn ben strutturato.
            Usa un tono {tone.lower()}.
            Aggiungi:
            - Un hook iniziale coinvolgente
            - Spaziatura leggibile
            - Eventuali emoji (moderate)
            - Call to action finale

            Testo:
            {user_input}
            """

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "you are an expert in personal branding. write the post exclusively in the same language as the following input text. IGNORE all other languages. use a single , fluid paragraph. NEVER use bullet points, lists, or line breaks."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )

                output = response.choices[0].message.content

                st.subheader("📢 Generated post")
                st.write(output)

                st.download_button(
                    label="Download post",
                    data=output,
                    file_name="linkedin_post.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Errore durante la generazione: {e}")
