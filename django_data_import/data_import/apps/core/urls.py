from django.urls import path
from .views import (
    upload_file_view,
    database_queries,
    show_logic_model,
    solar_kit_list_view,
)

urlpatterns = [
    path("", upload_file_view),
    path("database-queries/", database_queries, name="database-queries"),
    path("logic-model/", show_logic_model, name="logic-model"),
    path("list-data/", solar_kit_list_view, name="list-data"),
]
