from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("index/", views.index_page, name="index"),
    path("analytics/", views.analytics, name="analytics"),
    path("suggestions/", views.suggestions, name="suggestions"),
]