from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Poll


class PollListView(ListView):
    """Список всех голосований."""
    model = Poll
    template_name = 'polls/poll_list.html'
    context_object_name = 'polls'


class PollSearchView(ListView):
    """Страница поиска голосований."""
    model = Poll
    template_name = 'polls/poll_search.html'
    context_object_name = 'polls'
    
    def get_queryset(self):
        queryset = Poll.objects.all()
        
        # Фильтр по дате начала
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(pub_date__gte=date_from)
        
        # Фильтр по дате окончания
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(pub_date__lte=date_to)
        
        # Поиск по тексту вопроса
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(question__icontains=search_query)
        
        return queryset

