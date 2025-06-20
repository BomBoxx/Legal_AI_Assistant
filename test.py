import chromadb

# Initialize the persistent client
client = chromadb.PersistentClient(path="chroma_store")

# Get the collection
collection = client.get_collection("laws_document")

# Fetch all items in the collection
results = collection.get()

# Write results to a text file
with open("laws_output.txt", "w", encoding="utf-8") as file:
    file.write("Results from ChromaDB 'laws_document' collection:\n\n")
    for i in range(len(results["ids"])):
        file.write(f"ID: {results['ids'][i]}\n")
        file.write(f"Document: {results['documents'][i]}\n")
        if "metadatas" in results:
            file.write(f"Metadata: {results['metadatas'][i]}\n")
        file.write("\n" + "-"*40 + "\n\n")

print("Results saved to laws_output.txt")
