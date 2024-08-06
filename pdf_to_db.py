from process_files.extract_pdf import read_local_pdf
from supabase_functions.add_embedding_to_db import convert_and_add_data_to_supabase

# get list of pdf files in sample_pdfs folder
import os

pdf_files = [f for f in os.listdir("sample_data") if f.endswith(".pdf")]

# keep only last one
pdf_files = pdf_files[-1:]

# read each pdf file and convert to text
for pdf_file in pdf_files:
    print(f"Processing {pdf_file}")
    text = read_local_pdf(f"sample_data/{pdf_file}")
    convert_and_add_data_to_supabase(text, source=pdf_file)
    print(f"Processed {pdf_file}")

print("All PDFs processed")

