from __future__ import annotations

import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.question_text

    def was_published_recently(self) -> bool:
        """
        Return True if the question was published within the last day.

        This logic is intentionally the same as in the Django tutorial, including
        the boundary conditions that are covered by tests in part 5.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.choice_text



