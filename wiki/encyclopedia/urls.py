from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new", views.newPage, name = "newPage"),
    path("wiki/random", views.randomPage, name = "randomPage"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.editPage, name = "editPage"),
]
