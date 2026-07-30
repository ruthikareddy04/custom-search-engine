from django.db.models import Count
from .models import Term
from django.shortcuts import render
from .models import Document, DocumentTermFrequency, SearchHistory
from .crawler import index_multiple_pages
from django.http import JsonResponse
import math
import time
import requests


def search(request):
    query = request.GET.get("q", "").strip()

    results = []
    search_time = 0

    if query:
        response = requests.post(
    "https://custom-search-engine-production.up.railway.app/search",
    json={"query": query},
    timeout=30
)

        data = response.json()

        for item in data["results"]:
            results.append(
                (
                    item,
                    item["score"]
                )
            )

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