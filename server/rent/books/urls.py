from rest_framework import routers
from django.urls import path

from .views import BookViewSet, TagListApiView, GenreListApiView


router = routers.SimpleRouter()

router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('tags/', TagListApiView.as_view()),
    path('genres/', GenreListApiView.as_view()),
]

urlpatterns += router.urls
