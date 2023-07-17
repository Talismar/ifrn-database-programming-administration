from django.forms import Form, FileField


class UploadFileForm(Form):
    file = FileField()
