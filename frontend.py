import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG App", layout="wide")
st.title("📚 RAG App with Citations")

# -----------------------------
# Upload Section
# -----------------------------

st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / TXT / MD",
    type=["txt", "md", "pdf"]
)

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        st.sidebar.success("Uploaded successfully!")

# -----------------------------
# Document List + Delete
# -----------------------------

st.sidebar.header("Documents")

docs = requests.get(f"{API_URL}/documents").json()

for doc in docs:
    col1, col2 = st.sidebar.columns([4, 1])
    col1.write(f"📄 {doc['name']}")
    if col2.button("❌", key=doc["id"]):
        requests.delete(f"{API_URL}/documents/{doc['id']}")
        st.rerun()

# -----------------------------
# Chat Section
# -----------------------------

st.header("Ask a Question")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask something about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    if response.status_code == 200:
        data = response.json()
        answer = data["answer"]
        citations = data["citations"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("📌 Show Sources"):
                for c in citations:
                    st.markdown(f"**{c['label']}**")
                    st.write(c["snippet"])
    else:
        st.error("Error getting answer")