from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncomeListView.as_view(), name='income_list'),
    path('create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('<int:pk>/edit/', views.IncomeUpdateView.as_view(), name='income_edit'),
    path('<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='income_delete'),
]
