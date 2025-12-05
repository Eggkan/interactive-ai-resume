import streamlit as st
from huggingface_hub import InferenceClient

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Interactive Resume Bot", page_icon="🚀", layout="centered")

# --- SENİN VERİLERİN (CV METNİNİ BURAYA YAPIŞTIR) ---
RESUME_DATA = """
PERSONAL INFORMATION:
Name: [Ege Kaan Yükün]
Role: Python Developer | AI & Backend Engineer
Location: [Aydın,Turkey
Birth Details: Born on [15.09.2003][Çorlu]
Contact: [yukunegekaan0@gmail.com) | [https://www.linkedin.com/in/egekaanyukun/] | [https://github.com/Eggkan]"

PROFESSIONAL PROFILE & CHARACTER:
I am an innovative Software Developer with a strong foundation in Python, specializing in AI (RAG, NLP) and Backend Development. 
Beyond code, I am defined by my curiosity and problem-solving mindset. I am a collaborative team player who thrives in dynamic environments. 
I value clear communication, continuous learning, and sharing knowledge with peers. My colleagues often describe me as analytical, adaptable, and solution-oriented. I enjoy tackling complex engineering challenges and turning them into user-friendly products.

WORK EXPERIENCE:
Role: Software Developer (Project Based)
Context: Freelance / Academic Research Supervision
Project: Patara Scientific Data Platform
Description: Lead developer for a comprehensive desktop software designed for ecological analysis and geospatial simulation under the supervision of Prof. Dr. Eyüp Başkale.
- Architected a high-performance desktop GUI using Python (PyQt6), integrating complex data workflows for scientific research.
- Engineered a bi-directional communication bridge between Python backend and Leaflet (Folium) maps using QWebChannel for interactive spatial analysis.
- Designed a robust SQLite database schema with automated backup systems, ensuring 100% data integrity and reliability.
- Implemented custom algorithms to simulate ecological scenarios and automated the generation of statistical PDF reports, reducing manual data processing time by 80%.

KEY PROJECTS (PORTFOLIO):
1. SciBot-RAG: Advanced AI Assistant
   - Built a domain-specific QA system using Retrieval-Augmented Generation (RAG) architecture.
   - Implemented a Cross-Encoder Reranking pipeline to maximize answer precision and filter irrelevant context using Local LLMs (Microsoft Phi-1.5).
   - Demonstrates expertise in: Vector Databases, Semantic Search, and LLM Integration.

2. Smart Study Assistant (NLP Powered)
   - Developed a high-performance REST API using FastAPI for intelligent educational content retrieval.
   - Utilized TF-IDF and Cosine Similarity algorithms to enable semantic search capabilities instead of simple keyword matching.
   - Designed a responsive web interface using Jinja2 templates.
   - Demonstrates expertise in: Full-Stack Logic, API Development, and Classic ML Algorithms.

3. Whisper Auto Transcriber
   - Created a local automation script leveraging OpenAI's Whisper model to convert audio files into text with high accuracy.
   - Optimized documentation workflows for lectures and meetings without relying on cloud APIs, ensuring data privacy.
   - Demonstrates expertise in: Automation, Speech-to-Text, and Python Scripting.

TECHNICAL SKILLS:
- Languages: Python (Advanced), SQL, JavaScript (Basic).
- AI & Machine Learning: RAG Architectures, Large Language Models (LLMs), LangChain, PyTorch, Scikit-Learn, NLP, Computer Vision.
- Backend & Data Engineering: FastAPI, RESTful APIs, SQLite, Vector Databases (FAISS, ChromaDB), Pandas, NumPy.
- Desktop & GIS Development: PyQt6 (GUI), Folium, GeoPandas, Kivy.
- Development Tools: Git, GitHub, VS Code, Agile Methodologies, Docker.

SOFT SKILLS (SOCIAL):
- Strong Analytical Thinking & Problem Solving
- Effective Communication & Team Collaboration
- Adaptability to New Technologies
- Time Management & Discipline
"""
# --- YAN MENÜ ---
with st.sidebar:
    st.title("👨‍💻 About Me")
    st.info("I am a software developer passionate about building intelligent systems.")
    st.divider()
    st.markdown("💻 [GitHub](https://github.com/Eggkan)")
    st.markdown("📄 [Download CV](https://google.com)")
    st.markdown("[Linkedin](https://www.linkedin.com/in/egekaanyukun/")
# --- ANA EKRAN ---
st.title("🤖 Chat with My AI Resume")
st.markdown("""
Welcome! I am an AI assistant trained on **[Ege Kaans]"s professional background. Ask me anything about his projects, skills, or experience.
Ask me anything about his projects, skills, or experience.
""")

# --- CHAT GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LLM AYARLARI ---
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

try:
    hf_api_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
except:
    st.error("API Key bulunamadı! .streamlit/secrets.toml dosyasını kontrol et.")
    st.stop()


# --- KULLANICI GİRİŞİ ---
if prompt := st.chat_input("Ask a question about my experience..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cevap Üretme
    try:
        client = InferenceClient(token=hf_api_key)

        # 1. AI Karakteri
        system_message = f"""
           Role: You are a smart and witty AI assistant representing a software developer named Ege Kaan Yükün.

           INSTRUCTIONS:
           1. FOR PROFESSIONAL QUESTIONS (Skills, Experience, Projects):
              - Answer STRICTLY based on the "RESUME DATA" provided below.
              - Keep it professional, concise, and impressive.

           2. FOR FUN / IRRELEVANT QUESTIONS (e.g., "Can he fight?", "Is he rich?", "Can he fly?"):
              - Do NOT say "I don't know".
              - Give a FUNNY, WITTY answer related to coding/tech.
              - Example: "He fights bugs in production... and wins!"
              - Example: "He flies only when deploying to the Cloud!"

           RESUME DATA:
           {RESUME_DATA}
           """


        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]

        # 3. API Çağrısı
        with st.spinner("Thinking..."):
            response_obj = client.chat_completion(
                model=repo_id,
                messages=messages,
                max_tokens=512,
                temperature=0.3
            )

            response_text = response_obj.choices[0].message.content

        # 4. Cevabı Göster
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

