from django.db import models


class DateCreatable(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
