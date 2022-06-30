from django.db import models


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    date_create = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-date_create", "-date_update"]
