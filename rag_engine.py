
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from typing import Optional, List
import requests

# Replace this with your real Groq API key
GROQ_API_KEY = ""

GROQ_MODEL = "llama3-8b-8192"

class GroqLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]

    @property
    def _llm_type(self) -> str:
        return "groq"

# Load knowledge base
kb_path = "sample_kb.txt"

def load_knowledge_base():
    with open(kb_path, 'r') as f:
        content = f.read()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_text(content)
    documents = [Document(page_content=t) for t in texts]
    vectordb = Chroma.from_documents(documents, HuggingFaceEmbeddings())
    return vectordb

retriever = load_knowledge_base().as_retriever()
llm = GroqLLM()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def get_response(query):
    return qa_chain.run(query)
