from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('seat/',index,name="seat"),
    path('occupied/',occupiedSeats,name="occupied_seat"),
    path('search/', SearchResultsView.as_view() , name="search_results"),
    path('trip/',displayList, name ='trip'),
    path('payment/',payment, name ='payment'),
    path('payment/',payment, name ='payment'),
    path('history/',history, name='history'),
    path('confirm/',confirm, name='confirm')
]