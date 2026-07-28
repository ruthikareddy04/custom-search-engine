from django.urls import path
from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("search/", views.search, name="search"),
    path("index/", views.index_page, name="index"),
    path("analytics/", views.analytics, name="analytics"),
]