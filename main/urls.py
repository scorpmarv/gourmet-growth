from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('transaction/<int:pk>', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('sequence/<int:pk>', views.SequenceDetailView.as_view(), name='sequence_detail'),
    path('process/', views.process_json, name='process_json'),
]