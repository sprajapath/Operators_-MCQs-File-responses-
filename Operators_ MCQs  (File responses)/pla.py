import os
import glob
import re
from collections import defaultdict
from fuzzywuzzy import fuzz

def extract_questions(text):
    """Extracts questions from the document using regex."""
    return re.findall(r'\d+\.\s(.*?)\?', text)

def read_documents(folder_path):
    """Reads all text from documents in the given folder."""
    files = glob.glob(os.path.join(folder_path, "*.txt"))  # Adjust extension if needed
    documents = {}
    
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            documents[file] = extract_questions(f.read())
    
    return documents

def check_repeated_questions(documents):
    """Checks for repeated questions within and across documents."""
    repeated_within_docs = {}
    repeated_across_docs = defaultdict(list)
    
    # Check within each document
    for doc, questions in documents.items():
        seen = set()
        repeated = set()
        for q in questions:
            if q in seen:
                repeated.add(q)
            seen.add(q)
        if repeated:
            repeated_within_docs[doc] = repeated
    
    # Check across documents using fuzzy matching
    all_questions = []
    doc_mapping = []
    for doc, questions in documents.items():
        for q in questions:
            for i, existing_q in enumerate(all_questions):
                if fuzz.ratio(q, existing_q) > 85:  # Adjust similarity threshold
                    repeated_across_docs[existing_q].append((q, doc))
            all_questions.append(q)
            doc_mapping.append(doc)
    
    return repeated_within_docs, repeated_across_docs

# Set your file path
folder_path = r"C:\Users\spraj\OneDrive\Desktop\Operators_ MCQs  (File responses)"

documents = read_documents(folder_path)
within_doc_repeats, across_doc_repeats = check_repeated_questions(documents)

if not within_doc_repeats and not across_doc_repeats:
    print("No repeated questions found.")
else:
    print("Repeated questions within documents:")
    for doc, questions in within_doc_repeats.items():
        print(f"{doc}:")
        for q in questions:
            print(f"  - {q}")

    print("\nRepeated questions across documents:")
    for original, duplicates in across_doc_repeats.items():
        print(f"Original: {original}")
        for dup, doc in duplicates:
            print(f"  Duplicate: {dup} (in {doc})")

