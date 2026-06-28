import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


DOCS_FOLDER = "RAG/docs"
DB_PATH = "RAG/faiss_index"

documents = []

print("=" * 50)
print("Loading PDF documents...")
print("=" * 50)

# Load every PDF from the docs folder
for file in os.listdir(DOCS_FOLDER):

    if file.lower().endswith(".pdf"):

        pdf_path = os.path.join(DOCS_FOLDER, file)

        print(f"Loading: {file}")

        loader = PyPDFLoader(pdf_path)

        pdf_docs = loader.load()

        print(f"   {len(pdf_docs)} pages loaded")

        documents.extend(pdf_docs)

print("\n")
print(f"Total Pages Loaded: {len(documents)}")

print("\nSplitting documents into chunks...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = splitter.split_documents(documents)

print(f"Created {len(docs)} chunks")

print("\nCreating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Building FAISS vector database...")

vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

vectorstore.save_local(DB_PATH)

print("\nFAISS index saved successfully!")
print("RAG database is ready.")