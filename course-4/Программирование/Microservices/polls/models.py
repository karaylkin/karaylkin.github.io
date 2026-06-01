from django.db import models
from django.utils import timezone


class Poll(models.Model):
    """Модель голосования."""
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.question
    
    @property
    def total_votes(self):
        """Общее количество голосов."""
        return sum(choice.votes.count() for choice in self.choice_set.all())


class Choice(models.Model):
    """Модель варианта ответа."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Голосование')
    choice_text = models.CharField(max_length=200, verbose_name='Текст варианта')
    
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
    
    def __str__(self):
        return self.choice_text
    
    @property
    def vote_count(self):
        """Количество голосов за этот вариант."""
        return self.votes.count()


class Vote(models.Model):
    """Модель голоса (анонимная)."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes', verbose_name='Вариант')
    voted_at = models.DateTimeField(default=timezone.now, verbose_name='Время голосования')
    
    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        ordering = ['-voted_at']
    
    def __str__(self):
        return f"Голос за {self.choice.choice_text}"

