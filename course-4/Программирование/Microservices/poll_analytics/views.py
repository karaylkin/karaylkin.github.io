from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from polls.models import Poll, Choice, Vote
from django.db.models import Count
from django.http import HttpResponse
import json
import csv
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Используем backend без GUI
import matplotlib.pyplot as plt


class StatisticsView(APIView):
    """Микросервис 1: Статистика по голосованиям."""
    
    def get(self, request, poll_id):
        """Получить статистику по конкретному голосованию."""
        try:
            poll = get_object_or_404(Poll, id=poll_id)
            
            choices = poll.choice_set.annotate(annotated_vote_count=Count('votes')).all()
            total_votes = sum(choice.annotated_vote_count for choice in choices)
            
            choices_data = []
            for choice in choices:
                percentage = (choice.annotated_vote_count / total_votes * 100) if total_votes > 0 else 0.0
                choices_data.append({
                    'choice_text': choice.choice_text,
                    'vote_count': choice.annotated_vote_count,
                    'percentage': round(float(percentage), 2)
                })
            
            return Response({
                'poll_id': poll.id,
                'question': poll.question,
                'pub_date': poll.pub_date.isoformat(),
                'total_votes': total_votes,
                'choices': choices_data
            })
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении статистики: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PollsListView(APIView):
    """Микросервис 2: Сортировка и фильтрация голосований."""
    
    def get(self, request):
        """Получить список голосований с возможностью сортировки и фильтрации."""
        queryset = Poll.objects.all()
        
        # Фильтр по дате начала
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(pub_date__gte=date_from)
        
        # Фильтр по дате окончания
        date_to = request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(pub_date__lte=date_to)
        
        # Поиск по тексту
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(question__icontains=search)
        
        # Сортировка
        sort_by = request.query_params.get('sort_by', 'date')
        order = request.query_params.get('order', 'desc')
        
        if sort_by == 'date':
            if order == 'asc':
                queryset = queryset.order_by('pub_date')
            else:
                queryset = queryset.order_by('-pub_date')
        elif sort_by == 'popularity':
            # Сортировка по количеству голосов
            queryset = queryset.annotate(
                total_votes_count=Count('choice__votes')
            ).order_by('-total_votes_count' if order == 'desc' else 'total_votes_count')
        elif sort_by == 'votes':
            # То же, что и popularity
            queryset = queryset.annotate(
                total_votes_count=Count('choice__votes')
            ).order_by('-total_votes_count' if order == 'desc' else 'total_votes_count')
        
        # Подсчет голосов для каждого голосования
        polls_data = []
        for poll in queryset:
            total_votes = sum(choice.votes.count() for choice in poll.choice_set.all())
            polls_data.append({
                'id': poll.id,
                'question': poll.question,
                'pub_date': poll.pub_date.isoformat(),
                'total_votes': total_votes
            })
        
        return Response({
            'count': len(polls_data),
            'results': polls_data
        })


class ChartView(APIView):
    """Микросервис 3: Графики и диаграммы."""
    
    def get(self, request, poll_id):
        """Создать столбчатую диаграмму с результатами голосования."""
        poll = get_object_or_404(Poll, id=poll_id)
        
        choices = poll.choice_set.annotate(annotated_vote_count=Count('votes')).all()
        
        if not choices.exists():
            return Response({
                'error': 'Нет вариантов ответа для отображения'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Подготовка данных
        choice_texts = [choice.choice_text for choice in choices]
        vote_counts = [choice.annotated_vote_count for choice in choices]
        total_votes = sum(vote_counts)
        percentages = [(count / total_votes * 100) if total_votes > 0 else 0 for count in vote_counts]
        
        # Создание диаграммы
        plt.figure(figsize=(10, 6))
        # Генерация цветов для столбцов
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140']
        bar_colors = [colors[i % len(colors)] for i in range(len(choice_texts))]
        bars = plt.bar(range(len(choice_texts)), percentages, color=bar_colors)
        
        # Настройка графика
        plt.title(f'Результаты голосования: {poll.question[:50]}', fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Варианты ответа', fontsize=12)
        plt.ylabel('Процент голосов (%)', fontsize=12)
        plt.xticks(range(len(choice_texts)), choice_texts, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Добавление значений на столбцы
        for i, (bar, count, pct) in enumerate(zip(bars, vote_counts, percentages)):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count} ({pct:.1f}%)',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # Сохранение в base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        return Response({
            'poll_id': poll.id,
            'question': poll.question,
            'chart_base64': chart_base64,
            'data': {
                'choices': choice_texts,
                'votes': vote_counts,
                'percentages': [round(p, 2) for p in percentages]
            }
        })