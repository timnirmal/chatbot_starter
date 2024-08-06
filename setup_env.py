import os

from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from supabase.client import Client, create_client
from langsmith.wrappers import wrap_openai

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_anon_key = os.environ.get("SUPABASE_KEY")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Set OpenAI API key
openai_api_key = os.environ.get("OPENAI_KEY")
openai = wrap_openai(OpenAI(api_key=openai_api_key))

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-large", dimensions=3072)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)
