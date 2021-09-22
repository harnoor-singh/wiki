from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("searchResults/", views.searchResults, name="searchResults"),
    path("createNewPage/", views.createNewPage, name="createNewPage"),
    path("saveCreatedEntry/", views.saveCreatedEntry, name="saveCreatedEntry"),
    path("editEntry/<str:title>/", views.editEntry, name="editEntry"),
    path("saveEditedEntry/", views.saveEditedEntry, name="saveEditedEntry"),
    path("randomPage/", views.randomPage, name="randomPage"),
    path("<str:title>/", views.displayEntry, name="displayEntry")
]
