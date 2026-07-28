from django.contrib import admin
from .models import Document, Term, DocumentTermFrequency, SearchHistory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url")
    search_fields = ("title", "url")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)


@admin.register(DocumentTermFrequency)
class DocumentTermFrequencyAdmin(admin.ModelAdmin):
    list_display = ("document", "term", "frequency")
    search_fields = ("document__title", "term__word")


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("query", "results_count", "searched_at")
    search_fields = ("query",)
    list_filter = ("searched_at",)