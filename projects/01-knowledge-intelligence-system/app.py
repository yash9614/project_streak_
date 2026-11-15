import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA

load_dotenv()

st.set_page_config(page_title="Knowledge Intelligence System", page_icon="📚")
st.title("📚 Knowledge Intelligence System")
st.caption("Upload documents and ask questions (RAG)")

# Session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Sidebar - Upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing..."):
            docs = []
            for file in uploaded_files:
                temp_path = f"data/{file.name}"
                os.makedirs("data", exist_ok=True)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                
                if file.name.endswith(".pdf"):
                    loader = PyPDFLoader(temp_path)
                else:
                    loader = TextLoader(temp_path)
                docs.extend(loader.load())

            # Chunk
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            # Embed + Store
            embeddings = OpenAIEmbeddings()
            st.session_state.vectorstore = Chroma.from_documents(
                chunks, embeddings, persist_directory="chroma_db"
            )
            st.success(f"Processed {len(chunks)} chunks!")

# Chat
if st.session_state.vectorstore:
    query = st.chat_input("Ask a question about your documents...")
    if query:
        with st.spinner("Thinking..."):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
            )
            answer = qa.invoke(query)
            st.chat_message("user").write(query)
            st.chat_message("assistant").write(answer["result"])
else:
    st.info("Upload and process documents from the sidebar to start.")