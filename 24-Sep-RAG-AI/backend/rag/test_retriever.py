from retriever import retrieve_relevant_chunks


question = "What is the cancellation policy?"

results = retrieve_relevant_chunks(question)


print("\n========== RETRIEVED CHUNKS ==========\n")

documents = results["documents"][0]

for index, document in enumerate(documents, start=1):
    print(f"\n----- Result {index} -----\n")
    print(document)

print("\n=======================================\n")