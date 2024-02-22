from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("edit", views.editEntry, name="edit"),
    path("create", views.createEntry, name="create"),
    path("random", views.randomPage, name="random")
]
