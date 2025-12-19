import streamlit as st
import uuid
import os
from collections import defaultdict

from backend.pdf_parser import extract_sections, load_pdf_text
from backend.models import ResearchPaper
from backend.vector_store import index_papers, semantic_search

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Research AI", layout="wide")
st.title("📚 Research Paper Intelligence System")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "papers" not in st.session_state:
    st.session_state.papers = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = set()

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# SIDEBAR (UPLOAD + INDEX)
# -----------------------------
with st.sidebar:
    st.header("📄 Upload Research Paper")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_uploader"
    )

    if uploaded_file is not None:
        if uploaded_file.name not in st.session_state.uploaded_files:
            os.makedirs("data/papers", exist_ok=True)

            paper_id = str(uuid.uuid4())
            pdf_path = f"data/papers/{uploaded_file.name}"

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.read())

            full_text = load_pdf_text(pdf_path)
            sections = extract_sections(pdf_path)

            paper = ResearchPaper(
                paper_id=paper_id,
                title=uploaded_file.name.replace(".pdf", ""),
                authors=["Unknown"],
                abstract=sections[0].content if sections else "",
                full_text=full_text,
                year=2024,
                venue="arXiv",
                keywords=[],
                sections=sections,
                references=[]
            )

            st.session_state.papers.append(paper)
            st.session_state.uploaded_files.add(uploaded_file.name)
            st.session_state.indexed = False

            st.success("✅ Paper ingested successfully!")

            st.subheader("Detected Sections")
            for sec in sections:
                st.markdown(f"- {sec.title}")

        else:
            st.info("ℹ️ This paper is already uploaded.")

    st.divider()

    st.header("📦 Index Papers")
    if st.button("Index All Papers", key="index_button"):
        if st.session_state.papers:
            index_papers(st.session_state.papers)
            st.session_state.indexed = True
            st.success("🚀 Papers indexed into FAISS!")
        else:
            st.warning("⚠️ No papers available")

# -----------------------------
# CHAT UI
# -----------------------------
st.header("💬 Research Assistant")

# Display chat history (FULL)
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask something about the uploaded papers...")

# -----------------------------
# CHAT LOGIC
# -----------------------------
if query:
    # USER MESSAGE
    st.session_state.chat_history.append(
        {"role": "user", "content": query}
    )
    with st.chat_message("user"):
        st.markdown(query)

    query_lower = query.lower().strip()
    assistant_response = ""  # 🔑 store full output

    with st.chat_message("assistant"):

        # ----------------------------------
        # CASE 1: SHOW FULL PAPER
        # ----------------------------------
        if query_lower in ["show the paper", "show paper", "show full paper"]:
            if not st.session_state.papers:
                assistant_response = "No papers uploaded."
                st.warning(assistant_response)
            else:
                for paper in st.session_state.papers:
                    st.markdown(f"# 📄 {paper.title}")
                    assistant_response += f"# {paper.title}\n\n"

                    for sec in paper.sections:
                        st.markdown(f"## {sec.title}")
                        st.write(sec.content[:2000])

                        assistant_response += (
                            f"## {sec.title}\n"
                            f"{sec.content[:2000]}\n\n"
                        )

        # ----------------------------------
        # CASE 2: SEMANTIC SEARCH
        # ----------------------------------
        else:
            if not st.session_state.indexed:
                assistant_response = "⚠️ Please index papers first."
                st.warning(assistant_response)
            else:
                results = semantic_search(query)

                if not results:
                    assistant_response = "No results found."
                    st.info(assistant_response)
                else:
                    grouped = defaultdict(list)
                    for r in results:
                        grouped[r.metadata["paper_id"]].append(r)

                    for paper_id, chunks in grouped.items():
                        st.markdown(f"### 📄 Paper ID: {paper_id}")
                        assistant_response += f"### Paper ID: {paper_id}\n\n"

                        for c in chunks:
                            text = (
                                f"**Section:** {c.metadata.get('section', 'Unknown')}\n\n"
                                f"{c.page_content[:300]}...\n\n"
                            )
                            st.markdown(text)
                            assistant_response += text

    # ✅ STORE FULL ASSISTANT MESSAGE
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )
