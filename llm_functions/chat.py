import json
import os

from openai import OpenAI

from setup_env import vector_store, supabase
from supabase_functions.add_embedding_to_db import perform_similarity_search
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langsmith.wrappers import wrap_openai

openai_client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEYS")))



def get_context(query, file_id):
    docs = perform_similarity_search(vector_store, query, file_id)

    print(docs)
    return docs[0].page_content


def format_chat_history(chat_history):
    formatted_history = ""
    for i, entry in enumerate(chat_history):
        formatted_history += f"{entry['role']} : {entry['content']}\n"
        # Check if the next entry is from the same role, if not print a blank line
        if i + 1 < len(chat_history) and chat_history[i + 1]['role'] != entry['role']:
            # formatted_history += "\n"
            pass
    return formatted_history


def get_history(session_id):
    response = supabase.table("chat_message").select("*").eq("session_id", session_id).execute()

    data = response.data

    # Sort the data by the created_at timestamp to maintain the correct order
    sorted_data = sorted(data, key=lambda x: x['created_at'])

    # Extract the messages and their roles
    chat_history = []
    for entry in sorted_data:
        role = entry['role']
        message = entry['message']
        chat_history.append({'role': role, 'content': message})

    formatted_history = format_chat_history(chat_history)
    print(formatted_history)

    return formatted_history




def think(question: str, file_id: str, model: str, session_id: str):
    print("Generating Message", question)
    context = get_context(question, file_id)
    history = get_history(session_id)
    print(history)

    openai_client.api_key = os.environ.get("OPENAI_KEYS")

    openai_stream = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot named 'LawMate'. You are helping a user with their query related to law partcualarly in Sri Lanka.\n\n"
            },
            {
                "role": "user",
                "content": f"Question: \n{question}\n\n"
                           f"Context: \n{context}\n\n"
                           f"Chat History: \n{history}\n\n"
                           f"Answer:"
            }
        ],
        temperature=0.0,
        stream=True,
    )

    for event in openai_stream:
        if event.choices[0].delta.content is not None:
            print(event.choices[0].delta.content, end="")
            yield f"data: {json.dumps({'message': event.choices[0].delta.content})}\n\n"



def demo_think(question: str):
    openai_client.api_key = os.environ.get("OPENAI_KEYS")

    openai_stream = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot named 'LawMate'. You are helping a user with their query related to law partcualarly in Sri Lanka.\n\n"
            },
            {
                "role": "user",
                "content": f"Question: \n{question}\n\n"
                           f"Answer:"
            }
        ],
        temperature=0.0,
        stream=True,
    )

    for event in openai_stream:
        if event.choices[0].delta.content is not None:
            print(event.choices[0].delta.content, end="")
            yield f"data: {json.dumps({'message': event.choices[0].delta.content})}\n\n"