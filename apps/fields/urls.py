from django.urls import path
from .views import FieldCreateView, FieldListView, FieldDetailView, FieldUpdateDeleteView, AvailableFieldListView

urlpatterns = [
    path("create/", FieldCreateView.as_view(), name="field-create"),
    path("list/", FieldListView.as_view(), name="field-list"),
    path("available/", AvailableFieldListView.as_view(), name="available-fields"),
    path("<int:pk>/", FieldDetailView.as_view(), name="field-detail"),
    path("<int:pk>/edit/", FieldUpdateDeleteView.as_view(), name="field-update-delete"),
]
