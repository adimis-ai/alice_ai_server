import json

def get_all_docs_by_filters(collection_name, filters):
    try:
        return list(collection_name.find(filters))
    except Exception as e:
        print("Error:", e)

def get_n_docs_by_filters(collection_name, filters, n):
    try:
        return list(collection_name.find(filters).limit(n))
    except Exception as e:
        print("Error:", e)

def insert_doc(collection_name, doc):
    try:
        collection_name.insert_one(doc)
        print("Document inserted successfully!")
    except Exception as e:
        print("Error:", e)

def get_n_docs(collection_name, limit):
    try:
        last_docs = collection_name.find().sort("_id", -1).limit(limit)
        return list(last_docs)
    except Exception as e:
        print("Error:", e)

def display_prompt_by_user(collection_name, user_email):
    try:
        docs = collection_name.find({"email": user_email})
        docs = list(docs)
        docs = [json.dumps(doc, default=str) for doc in docs]
        return docs
    except Exception as e:
        print("Error:", e)
