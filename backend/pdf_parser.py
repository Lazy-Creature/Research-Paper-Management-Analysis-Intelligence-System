from pypdf import PdfReader
import re
from backend.models import PaperSection

SECTION_MAP = {
    "abstract": "Abstract",
    "index terms": "Index Terms",
    "introduction": "Introduction",
    "background": "Introduction",
    "related work": "Related Work",
    "method": "Methodology",
    "methods": "Methodology",
    "methodology": "Methodology",
    "approach": "Methodology",
    "experiment": "Experiments",
    "experiments": "Experiments",
    "evaluation": "Experiments",
    "results": "Results",
    "discussion": "Discussion",
    "conclusion": "Conclusion",
    "conclusions": "Conclusion",
    "references": "References",
}

# Matches:
# IV. METHODOLOGY
# 3. Experiments
# Abstract—
# Index Terms—
SECTION_HEADER_REGEX = re.compile(
    r"""
    ^\s*
    (?:[IVX]+\.|\d+\.|\d+\.\d+)?      # Roman or numeric prefix
    \s*
    (abstract|index\s+terms|introduction|background|related\s+work|
     methodology|methods?|approach|
     experiments?|evaluation|results?|discussion|
     conclusions?|references)
    \b
    """,
    re.IGNORECASE | re.VERBOSE
)

INLINE_HEADER_REGEX = re.compile(
    r"^(abstract|index\s+terms)\s*[-—:]", re.IGNORECASE
)

def load_pdf_text(pdf_path: str):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def clean_text(text: str):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_sections(pdf_path: str):
    text = load_pdf_text(pdf_path)
    lines = text.split("\n")

    sections = []
    buffer = []
    current_section = "Front Matter"
    order = 0

    for line in lines:
        line_clean = line.strip()

        inline_match = INLINE_HEADER_REGEX.match(line_clean.lower())
        header_match = SECTION_HEADER_REGEX.match(line_clean.lower())

        if inline_match or header_match:
            # Save previous section
            if buffer:
                sections.append(
                    PaperSection(
                        section_id=f"sec_{order}",
                        title=current_section,
                        content=clean_text(" ".join(buffer)),
                        order=order
                    )
                )
                order += 1
                buffer = []

            header = (inline_match or header_match).group(1).lower()
            current_section = SECTION_MAP.get(header, header.title())
        else:
            buffer.append(line_clean)

    if buffer:
        sections.append(
            PaperSection(
                section_id=f"sec_{order}",
                title=current_section,
                content=clean_text(" ".join(buffer)),
                order=order
            )
        )

    # Remove junk sections
    sections= [
        s for s in sections
        if len(s.content) > 400 and s.title != "Front Matter"
    ]

    return sections
