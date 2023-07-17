from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import UploadFileForm
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
import pandas as pd
from .models import SolarKit
from django.db import connection
from .use_case.data_import_use_case import DataImportUseCase


csv_content_type: str = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


class UploadFileView(View):
    template_name = "upload.html"

    def get(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponse:
        return render(request, self.template_name)

    def post(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponse:
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["file"]

            if file.content_type == csv_content_type:
                df = pd.read_excel(file, sheet_name="Kit Ipojuca")
                import_data_use_case = DataImportUseCase(df)
                import_data_use_case.run()

                messages.success(request, "File uploaded successfully")
            else:
                messages.error(request, "File upload failed.")
        else:
            messages.error(request, "File upload failed.")

        return render(request, self.template_name)


def database_queries(request: HttpRequest) -> HttpResponse:
    data: list = []
    columns: list = []

    if request.method == "POST":
        with connection.cursor() as cursor:
            try:
                cursor.execute(request.POST.get("sql-code"))
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
            except Exception:
                pass
            finally:
                cursor.close()

    return render(
        request, "database_queries.html", {"data": data, "columns": columns}
    )


def show_logic_model(request: HttpRequest) -> HttpResponse:
    return render(request, "logic_model.html")


class SolarKitListView(ListView):
    model = SolarKit
    paginate_by = 12
    template_name = "list_data.html"


upload_file_view = UploadFileView.as_view()
solar_kit_list_view = SolarKitListView.as_view()
