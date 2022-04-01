from django.urls import path
from . import handlers


urlpatterns = [
    path("questions", handlers.questions_handler),
    path("answers", handlers.answers_handler),
]
