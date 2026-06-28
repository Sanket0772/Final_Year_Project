from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_chatbot():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        "RAG/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    generator = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )

    return retriever, generator


def ask_question(question):
    retriever, generator = load_chatbot()

    docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a desiccant dehumidifier maintenance assistant.
Answer ONLY from the provided context.

If answer is unavailable, say:
I could not find that information in the manual.

Context:
{context}

Question:
{question}

Answer:
"""

    response = generator(
        prompt,
        max_new_tokens=120,
        do_sample=False
    )

    generated = response[0]["generated_text"]
    answer = generated.replace(prompt, "").strip()

    return answer