import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


# -------------------------------
# Load Gemini API key
# -------------------------------
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


# -------------------------------
# 1. Extract text from uploaded PDF
# -------------------------------
def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text.strip()


# -------------------------------
# 2. Split text into chunks
# -------------------------------
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300
    )
    chunks = text_splitter.split_text(text)

    # limit chunks to reduce Gemini embedding quota usage
    return chunks[:20]


# -------------------------------
# 3. Create FAISS vector store
# -------------------------------
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store


# -------------------------------
# 4. Answer user question
# -------------------------------
def answer_question(user_question, vector_store):
    docs = vector_store.similarity_search(user_question, k=4)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt_template = """
Answer the question as clearly as possible using only the provided context.
If the answer is not present in the context, say:
"Answer is not available in the provided PDF."

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    final_prompt = prompt.format(context=context, question=user_question)

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        google_api_key=google_api_key
    )

    response = model.invoke(final_prompt)
    return response.content


# -------------------------------
# 5. Main Streamlit App
# -------------------------------
def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon="📄")
    st.title("📄 Chat with PDF using LangChain")
    st.write("Upload a PDF, process it, and ask questions from it.")

    if not google_api_key:
        st.error("GOOGLE_API_KEY not found. Please add it in your .env file.")
        return

    pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

    if pdf_file is not None:
        if st.button("Process PDF"):
            try:
                with st.spinner("Processing PDF..."):
                    raw_text = get_pdf_text(pdf_file)

                    if not raw_text:
                        st.error("No readable text found in the PDF.")
                        return

                    text_chunks = get_text_chunks(raw_text)

                    if not text_chunks:
                        st.error("Could not create text chunks from the PDF.")
                        return

                    vector_store = get_vector_store(text_chunks)
                    st.session_state.vector_store = vector_store

                    st.success("PDF processed successfully!")

            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.error(
                        "Gemini API quota exceeded. Please wait 1 minute and try again, or use a smaller PDF."
                    )
                elif "404" in error_text or "NOT_FOUND" in error_text:
                    st.error("Embedding model/API issue. Please check your Gemini API key and model name.")
                else:
                    st.error(f"Error while processing PDF: {error_text}")

    user_question = st.text_input("Ask a question from the PDF")

    if user_question:
        if "vector_store" not in st.session_state:
            st.warning("Please upload and process a PDF first.")
        else:
            try:
                with st.spinner("Generating answer..."):
                    answer = answer_question(user_question, st.session_state.vector_store)
                    st.subheader("Answer")
                    st.write(answer)

            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.error("Gemini API quota exceeded while generating answer. Please wait and try again.")
                elif "404" in error_text or "NOT_FOUND" in error_text:
                    st.error("Gemini model not found. Try gemini-2.0-flash.")
                else:
                    st.error(f"Error while generating answer: {error_text}")


if __name__ == "__main__":
    main()