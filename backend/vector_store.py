from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from backend.chunking import chunk_paper

embeddings= HuggingFaceEmbeddings(
    model_name= "sentence-transformers/all-MiniLM-L6-v2"
)

VECTOR_DB= None

def index_papers(papers):
    global VECTOR_DB
    texts, metadatas= [], []

    for paper in papers:
        t, m= chunk_paper(paper)
        texts.extend(t)
        metadatas.extend(m)

    VECTOR_DB= FAISS.from_texts(
        texts= texts,
        embedding= embeddings,
        metadatas= metadatas
    )    
    return VECTOR_DB

def semantic_search(query, top_k=5):
    if VECTOR_DB is None:
        return []
    return VECTOR_DB.similarity_search(query, k=top_k)