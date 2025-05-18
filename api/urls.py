from django.urls import path
from .views import sentiment, summarizer

urlpatterns = [
    path('sentiment/', sentiment),
    path('summarizer/', summarizer)
]