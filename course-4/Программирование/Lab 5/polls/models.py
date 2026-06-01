from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField("Текст вопроса", max_length=255)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, related_name="questions", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField("Вариант ответа", max_length=255)
    votes = models.IntegerField("Голоса", default=0)

    def __str__(self) -> str:
        return self.choice_text


