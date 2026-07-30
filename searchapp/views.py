from django.db.models import Count
from django.shortcuts import render
from .models import Document, DocumentTermFrequency, SearchHistory, Term
from .crawler import index_multiple_pages
from django.http import JsonResponse
from math import log
import time


def search(request):
    query = request.GET.get("q", "").strip().lower()

    results = []
    search_time = 0

    if query:
        start = time.time()

        words = query.split()
        scores = {}

        total_documents = Document.objects.count()

        for word in words:

            records = DocumentTermFrequency.objects.filter(
                term__word__icontains=word
            )

            document_frequency = records.values("document").distinct().count()

            if document_frequency == 0:
                continue

            idf = log(total_documents / (1 + document_frequency))

            for record in records:

                doc = record.document

                tf = record.frequency

                tfidf = (1 + log(tf)) * idf

                if doc.id not in scores:
                    scores[doc.id] = {
                        "title": doc.title,
                        "url": doc.url,
                        "snippet": doc.snippet,
                        "score": 0,
                    }

                scores[doc.id]["score"] += tfidf

                if word in doc.title.lower():
                    scores[doc.id]["score"] += 50

                if word in doc.url.lower():
                    scores[doc.id]["score"] += 20

                if word in doc.snippet.lower():
                    scores[doc.id]["score"] += 10

        results = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True,
        )

        SearchHistory.objects.create(
            query=query,
            results_count=len(results)
        )

        search_time = round(time.time() - start, 3)

    return render(
        request,
        "search.html",
        {
            "query": query,
            "results": results,
            "search_time": search_time,
        },
    )
def index_page(request):
    message = ""

    if request.method == "POST":
        url = request.POST.get("url")

        if url:
            try:
                pages = index_multiple_pages(url, max_pages=10)
                message = f"Successfully indexed {pages} pages."
            except Exception as e:
                message = f"Error: {e}"

    return render(
        request,
        "index.html",
        {
            "message": message,
        },
    )
def analytics(request):

    total_documents = Document.objects.count()

    total_terms = Term.objects.count()

    total_searches = SearchHistory.objects.count()

    top_searches = (
        SearchHistory.objects
        .values("query")
        .annotate(count=Count("query"))
        .order_by("-count")[:10]
    )

    recent_searches = (
        SearchHistory.objects
        .order_by("-searched_at")[:10]
    )

    return render(
        request,
        "analytics.html",
        {
            "total_documents": total_documents,
            "total_terms": total_terms,
            "total_searches": total_searches,
            "top_searches": top_searches,
            "recent_searches": recent_searches,
        },
    )
def home(request):
    return render(request, "home.html")
def suggestions(request):

    q = request.GET.get("q", "").lower()

    suggestions = []

    if q:

        terms = (
            Term.objects
            .filter(word__startswith=q)
            .values_list("word", flat=True)
            .distinct()[:10]
        )

        suggestions = list(terms)

    return JsonResponse(suggestions, safe=False)