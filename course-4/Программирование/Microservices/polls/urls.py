from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollListView.as_view(), name='poll_list'),
    path('search/', views.PollSearchView.as_view(), name='poll_search'),
]

