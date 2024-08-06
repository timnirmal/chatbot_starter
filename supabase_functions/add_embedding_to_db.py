from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import SupabaseVectorStore
from setup_env import embeddings, supabase


def load_and_split_documents(filename: str, chunk_size: int = 1000, chunk_overlap: int = 50):
    loader = TextLoader(filename, encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="\n")
    # print(text_splitter)
    split_docs = text_splitter.split_documents(documents)
    print(len(split_docs))

    return split_docs


def add_documents_to_vector_store(split_docs, embeddings, client, table_name: str, query_name: str, user_id: str = None,
                                  source: str = None, chunk_size: int = 500):
    vector_store_upload = SupabaseVectorStore.from_documents(
        split_docs,
        embeddings,
        client=client,
        table_name=table_name,
        query_name=query_name,
        chunk_size=chunk_size,
        metadata={"source": source, "user_id": user_id}
    )
    return vector_store_upload


def perform_similarity_search(vector_store, query: str, file_id: str):
    matched_docs = vector_store.similarity_search(query, filter={"file_id": file_id})
    return matched_docs


def convert_and_add_data_to_supabase(text, source=""):
    # save in temp txt file
    with open("temp_files/temp_embedding.txt", "w", encoding="utf-8") as file:
        file.write(text)
    split_docs = load_and_split_documents("temp_files/temp_embedding.txt")

    split_docs[0].metadata['source'] = source
    # print(split_docs)

    # for i in range(len(split_docs)):
    #     print(split_docs[i].page_content + "...")

    print(len(split_docs))
    # print(split_docs[0].page_content[:1000] + "...")
    # print(split_docs[0])
    a = add_documents_to_vector_store(split_docs, embeddings, supabase, "documents", "match_documents")
    # vector_store.upload(client, table_name=table_name, query_name=query_name, metadata={"source": source})


# response = """More than anything, at Dilmah we believe in being kind. Kindness is at the heart of everything we do. We spread kindness by doing everything with care and respect."""
# convert_and_add_data_to_supabase(response, source="Dilmah Tea")
#
# convert_and_add_data_to_supabase("hey how are you", source="TIm TIm")

# TODO : Add file_id to the database
