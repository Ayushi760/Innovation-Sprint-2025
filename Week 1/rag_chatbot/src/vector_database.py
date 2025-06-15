import chromadb
from chromadb.utils import embedding_functions
from typing import List, Tuple, Dict, Any


class VectorDatabase:
    def __init__(self, persist_directory: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents_collection",
            embedding_function=self.sentence_transformer_ef
        )

    def get_collection(self):
        return self.collection

    def semantic_search(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def get_context_with_sources(self, results: Dict[str, Any]) -> Tuple[str, List[str]]:
        context = "\n\n".join(results['documents'][0])

        sources = [
            f"{meta['source']} (chunk {meta['chunk']})"
            for meta in results['metadatas'][0]
        ]

        return context, sources

    def print_search_results(self, results: Dict[str, Any]):
        print("\nSearch Results:\n" + "-" * 50)

        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            distance = results['distances'][0][i]

            print(f"\nResult {i + 1}")
            print(f"Source: {meta['source']}, Chunk {meta['chunk']}")
            print(f"Distance: {distance}")
            print(f"Content: {doc}\n")

    def get_collection_info(self) -> Dict[str, Any]:
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {"error": str(e)}

    def delete_collection(self):
        try:
            self.client.delete_collection(name="documents_collection")
            print("Collection deleted successfully")
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")

    def reset_collection(self):
        try:
            self.delete_collection()
            self.collection = self.client.get_or_create_collection(
                name="documents_collection",
                embedding_function=self.sentence_transformer_ef
            )
            print("Collection reset successfully")
        except Exception as e:
            print(f"Error resetting collection: {str(e)}")
