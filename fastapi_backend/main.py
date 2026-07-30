from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from django.db.models import Sum
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "custom_search_engine.settings"
)

import django
django.setup()

from searchapp.models import DocumentTermFrequency


app = FastAPI(
    title="Custom Search Engine API",
    version="1.0.0"
)


class SearchRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "FastAPI Backend Running"
    }


@app.post("/search")
def search(data: SearchRequest):

    query = data.query.lower().strip()
    words = query.split()

    scores = {}

    for word in words:

        records = DocumentTermFrequency.objects.filter(
            term__word=word
        )

        for record in records:

            doc = record.document

            if doc.id not in scores:

                scores[doc.id] = {
                    "title": doc.title,
                    "url": doc.url,
                    "snippet": doc.snippet,
                    "score": 0
                }

            scores[doc.id]["score"] += record.frequency

            if word in doc.title.lower():
                scores[doc.id]["score"] += 15

            if word in doc.snippet.lower():
                scores[doc.id]["score"] += 8

    results = sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }