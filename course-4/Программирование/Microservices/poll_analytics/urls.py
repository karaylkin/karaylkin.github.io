from django.urls import path
from . import views
from .export_views import ExportView

urlpatterns = [
    # Микросервис 1: Статистика по голосованиям
    path('polls/<int:poll_id>/statistics/', views.StatisticsView.as_view(), name='poll_statistics'),
    
    # Микросервис 3: Графики и диаграммы
    path('polls/<int:poll_id>/chart/', views.ChartView.as_view(), name='poll_chart'),
    
    # Микросервис 4: Экспорт данных (CSV и JSON)
    path('polls/<int:poll_id>/export/', ExportView.as_view(), name='poll_export'),
    
    # Микросервис 2: Сортировка и фильтрация (должен быть последним)
    path('polls/', views.PollsListView.as_view(), name='polls_list_filtered'),
]

