from django.urls import path
from apps.fields.views import FieldCreateView, FieldListView, FieldDetailView, FieldUpdateDeleteView

urlpatterns = [
    path("create/", FieldCreateView.as_view(), name="field-create"),
    path("list/", FieldListView.as_view(), name="field-list"),
    # path("all/", FieldAllView.as_view(), name="field-all"),
    path("<int:pk>/", FieldDetailView.as_view(), name="field-detail"),
    path("<int:pk>/", FieldUpdateDeleteView.as_view(), name="field-update-delete"),
]