from django.db.models import Count
from .models import Term
from django.shortcuts import render
from .models import Document, DocumentTermFrequency, SearchHistory
from .crawler import index_multiple_pages
import math
import time


def search(request):
    start_time = time.time()

    query = request.GET.get("q", "").strip().lower()

    results = {}

    total_documents = Document.objects.count()

    if query and total_documents > 0:

        words = query.split()

        for word in words:

            records = DocumentTermFrequency.objects.filter(
                term__word__icontains=word
            )

            document_frequency = records.values(
                "document"
            ).distinct().count()

            if document_frequency == 0:
                continue

            idf = math.log(total_documents / document_frequency)

            for record in records:

                document = record.document
                tf = record.frequency
                score = tf * idf

                if document not in results:
                    results[document] = 0

                results[document] += score

                # Title boost
                if word in document.title.lower():
                    results[document] += 20

                # URL boost
                if word in document.url.lower():
                    results[document] += 10

        # Round scores to 2 decimal places
        sorted_results = [
            (doc, round(score, 2))
            for doc, score in sorted(
                results.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]

        SearchHistory.objects.create(
            query=query,
            results_count=len(sorted_results)
        )

    else:
        sorted_results = []

    search_time = round(time.time() - start_time, 4)

    return render(
        request,
        "search.html",
        {
            "results": sorted_results,
            "query": query,
            "search_time": search_time,
            "recent_searches": SearchHistory.objects.order_by("-searched_at")[:5],
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