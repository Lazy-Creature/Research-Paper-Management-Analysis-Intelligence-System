from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter= RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

def chunk_paper(paper):
    texts= []
    metadatas= []

    for section in paper.sections:
        chunks= splitter.split_text(section.content)
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({
                "paper_id": paper.paper_id,
                "section": section.title,
                "year": paper.year,
                "keywords": paper.keywords
            })

    return texts, metadatas        