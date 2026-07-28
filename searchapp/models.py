from django.db import models


class Document(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=500)
    snippet = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Term(models.Model):
    word = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.word


class DocumentTermFrequency(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    def __str__(self):
        return f"{self.document.title} - {self.term.word}"


class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    results_count = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query