from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class DailyNote(models.Model):
    date = models.DateField(unique=True)
    # content = models.TextField(blank=True, null=True)
    content = CKEditor5Field('내용', config_name='extends', blank=True, null=True)

    def __str__(self):
        return f"{self.date}"
