import email
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import  csrf_exempt
from .models import *
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.core.mail import EmailMessage
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseForbidden
import json
# Create your views here.
class SearchResultsView(ListView):
  
    template_name = "trip.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        query2 = self.request.GET.get("s")
        object_list = Trip.objects.filter(
            Q(departure__icontains=query), Q(destination__icontains=query2)
        )
        return object_list

def index(request):
    trip=Trip.objects.all()
    return render(request,'index.html',{
        "trips":trip
    })

def history(request):
    current_user = request.user
    all_payment = Payment.objects.all()
    return render(request,'search_result.html',{
        "payments": all_payment,
        "user":current_user
    })

@csrf_exempt
def occupiedSeats(request):
    data=json.loads(request.body)
    trip=Trip.objects.get(product_name=data["trips"])
    occupied=trip.booked_seats.all()
    occupied_seat=list(map(lambda seat : seat.seat_no - 1,occupied))

    return JsonResponse({
        "occupied_seats":occupied_seat,
        "trip":str(trip)
    })

def displayList(request):
    Data =Trip.objects.all() #.order_by('-date')
    return render(request, 'trip.html',{ 
                'object_list': Data    }
    )

@csrf_exempt
def payment(request):
    data=json.loads(request.body)
    booked_seat=list(map(lambda seat: seat+1,data["seat_list"]))
    trip_name=data["trip_name"]

    cost=Trip.objects.get(product_name=trip_name).price
    trip=Trip.objects.get(product_name=trip_name)

    current_user = request.user
    
    seat_number = ''

    for seat_no in booked_seat:
        seat=Seat.objects.create(seat_no=seat_no,
        occupant_username=current_user.username,
        occupant_email=current_user.email)

        trip.booked_seats.add(seat)
        trip.save()

        Payment.objects.create(username=current_user.username,
        email=current_user.email,
        phone=current_user.phone_number,
        trip=trip,
        seat_no=seat_no)

        seat_number += str(seat_no)
        seat_number += ' '
        
    render_msg=render_to_string("book.html",{
        "first_name":current_user.username,
        "trip_name":trip_name,
        "trip_date":trip.start_date,
        "seat_no":seat_number
    })
    send_email = EmailMessage("[Booking group 5]:Thank you for purchasing a ticket",
                             render_msg, 
                             to=[current_user.email])
    send_email.send()
    return JsonResponse({
        'link': '/'
    })
def confirm(request):
    return render(request,'confirm.html')