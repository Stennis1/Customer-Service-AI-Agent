from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader


class KnowledgeBase:
    def __init__(self, data_path="./knowledge", persist_directory="./chromadb"):
        self.data_path = data_path
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = self._load_knowledge_base()


    def _load_documents(self):
        """Load documents from various sources"""
        txt_loader = DirectoryLoader(
            path=self.data_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            silent_errors=True
        )

        pdf_loader = DirectoryLoader(
            path=self.data_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            silent_errors=True
        )

        documents = []
        documents.extend(txt_loader.load())
        documents.extend(pdf_loader.load())
        return documents
    
    
    def _load_knowledge_base(self):
        """Load and index knowledge base documents."""
        documents = self._load_documents()
        if not documents:
            raise ValueError(
                f"No documents found under '{self.data_path}'. "
                "Add .txt/.pdf files before starting the agent."
            )

        chunks = self.text_splitter.split_documents(documents)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

        return vectorstore
    

    def search(self, query: str, k: int = 3) -> str:
        """Search knowledge base and return relevant information"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)

            if not docs:
                return "No relevant information found in the knowledge base"
            
            # Combine relevant chunks 
            combined_info = "\n\n".join([doc.page_content for doc in docs])
            return f"Based on our knowledge base:\n{combined_info}"

        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"


# Backward-compatible alias for old typoed class name.
KnowledegeBase = KnowledgeBase
