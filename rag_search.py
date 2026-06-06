import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df = pd.read_csv("match_data.csv")

documents = []

for _, row in df.iterrows():

    text = (
        f"Date: {row['date']}. "
        f"Series: {row['series']}. "
        f"Venue: {row['venue']}. "
        f"Result: {row['result']}."
    )

    documents.append(text)

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

while True:

    query = input(
        "\nEnter query (or exit): "
    )

    if query.lower() == "exit":
        break

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    top_k = np.argsort(
        similarities
    )[-3:][::-1]

    print("\nTop 3 Matches:\n")

    for idx in top_k:
        print(documents[idx])
        print("-" * 80)