import streamlit as st
from groq import Groq
import os

# Inizializza client Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

st.title("✍️ Generatore di Post LinkedIn con Groq")

st.write("Inserisci un testo grezzo e trasformalo in un post professionale per LinkedIn.")

# Input utente
user_input = st.text_area("Testo di partenza", height=200)

tone = st.selectbox(
    "Scegli il tono del post",
    ["Professionale", "Ispirazionale", "Informale", "Tecnico"]
)

if st.button("Genera Post"):
    if not user_input.strip():
        st.warning("Inserisci del testo prima di generare.")
    else:
        with st.spinner("Generazione in corso..."):

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
                    model="11ama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Sei un esperto di personal branding su LinkedIn."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )

                output = response.choices[0].message.content

                st.subheader("📢 Post Generato")
                st.write(output)

                st.download_button(
                    label="Scarica il post",
                    data=output,
                    file_name="linkedin_post.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Errore durante la generazione: {e}")
