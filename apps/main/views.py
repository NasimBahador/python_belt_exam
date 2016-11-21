from django.shortcuts import render, HttpResponse, redirect
from models import User, Trip
from django.contrib import messages


# Create your views here.
def session_check(request):
    if 'user' in request.session:
        return True
    else:
        return False

def index(request):
    
    context = {
        "user_trips": Trip.objects.filter(trip_creator=request.session['user_id'])| Trip.objects.filter(joiner=request.session['user_id']),
        "user": User.objects.get(id=request.session['user_id']),
        'trips': Trip.objects.all().exclude(trip_creator=request.session['user_id']).exclude(joiner=request.session['user_id']),
    }

    return render(request, "main/index.html", context)

def add_trip(request):
    return render(request, 'main/add.html')

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)

def create(request):
    errors = Trip.objects.add_trip(request.POST)
    if errors:
        print_errors(request, errors)
        return redirect('main:add_trip')
    else:
        Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], description=request.POST['description'], trip_creator=User.objects.get(id=request.session['user_id']))
    return redirect("main:index")

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    travel = Trip.objects.get(id=id)
    travel.joiner.add(user)
    return redirect("main:index")

def destination(request, id):
    context = {
    'trip': Trip.objects.get(id=id),
    'user': User.objects.get(id=request.session['user_id']),
    'buddies': User.objects.filter(travel_buddy=id),
    }
    return render(request, 'main/destination.html', context)



def logout(request):
    request.session.clear()
    return redirect('login:index')
