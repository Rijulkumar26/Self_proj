#  UHC Policy Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that helps doctors, clinics, and hospital staff query insurance policies from UnitedHealthcare (UHC) to understand coverage, criteria, and limitations.



##  How to Use (Step-by-Step)

1. Open the chatbot using the frontend URL
2. Enter your query in natural language (e.g., “Is spinal cord stimulation covered?”)
3. View:
   - Coverage details
   - When the procedure is not covered
   - Required criteria
   - Source policies


##  Example Queries

- Is spinal cord stimulation covered?
- What are the coverage criteria for MRI?
- When is bariatric surgery denied?
- What documentation is required for approval?


##  Architecture

###  High-Level Design (HLD)

User → Streamlit Frontend → FastAPI Backend → FAISS Vector DB → LLM (Gemini/OpenAI)


###  Low-Level Design (LLD)

#### 1. Data Pipeline
- Scraped UHC policy PDFs
- Extracted text using PyMuPDF
- Split into sections (coverage, criteria, etc.)
- Chunked into smaller segments

#### 2. Embeddings
- Model: BAAI/bge-small-en-v1.5
- Generated embeddings for each chunk
- Stored in FAISS index

#### 3. Retrieval
- Query converted to embedding
- FAISS retrieves top-k relevant chunks

#### 4. LLM Layer
- Gemini 2.5 Flash
- Generates structured responses:
  - Coverage
  - Not Covered
  - Criteria

#### 5. Frontend
- Streamlit chat interface
- Displays answers + sources


##  Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Backend     | FastAPI |
| Frontend    | Streamlit |
| Embeddings  | BGE (HuggingFace) |
| Vector DB   | FAISS |
| LLM         | Gemini|
| Scraping    | BeautifulSoup |
| PDF Parsing | PyMuPDF |
