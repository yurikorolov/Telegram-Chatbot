import chromadb
from chromadb.db.base import UniqueConstraintError


class Memory:
    def __init__(self, name):
        self.name = name
        self.client = chromadb.PersistentClient(
            path="./persist"
        )
        try:
            self.collection = self.client.create_collection(name)
        except UniqueConstraintError:
            self.collection = self.client.get_collection(name)
        except Exception as e:
            print(f"Error initializing Memory class: {e}")
            raise

    def insert(self, data, uuid):
        # Check for existing duplicates
        existing = self.collection.get(ids=[uuid], include=["documents"])
        if not existing["documents"] or data not in existing["documents"]:
            self.collection.add(documents=[data], ids=[uuid])

    def find(self, query):
        # Get current collection count
        count = self.collection.count()
        n_results = min(2, count) if count > 0 else 1
        q = self.collection.query(query_texts=[query], n_results=n_results)
        return q["documents"]
