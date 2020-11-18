from django.shortcuts import render, redirect
from .models import User, Travel
from django.contrib import messages
import bcrypt

def register_login(request):
    return render(request, "register_login.html")

def register(request):
    print(request.POST)
    print("%" *70)
    print(User.objects.reg_validator(request.POST))
    print("%" *70)
    
    #check if register object is valid
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags =key)
        return redirect("/")

    #check to see if email is in use
    user = User.objects.filter(email=request.POST['emailReg'])
    if user:
        messages.error(request, "Email is already in use.", extra_tags ="emailReg" )
        return redirect("/")

    #hash the password with bcrypt
    pw = bcrypt.hashpw(request.POST['passwordReg'].encode(),bcrypt.gensalt()).decode()

    #create user in database
    User.objects.create(
        firstname = request.POST['firstnameReg'],
        lastname = request.POST['lastnameReg'],
        email = request.POST['emailReg'],
        password = pw
    )

    # put user id into session and redirect
    request.session['user_id'] = User.objects.last().id
    return redirect("/dashboard")

    return redirect("/")

def login(request):
    #check if POST request
    if request.method == "POST":
        #validate login
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        #check if email is in database
        user = User.objects.filter(email=request.POST['loginEmail'])
        if len(user) == 0:
            messages.error(request, "Invalid Email\Password" , extra_tags="login")
            return redirect("/")
        #check if passwords match
        if not bcrypt.checkpw(request.POST['loginPassword'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email\Password", extra_tags="login")
            return redirect("/")
        #put user id into session and redirect
        request.session['user_id'] = user[0].id
        return redirect("/dashboard")
    else:
        return redirect("/")

    return redirect("/dashboard")

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

    return redirect("/")

def dashboard(request):
    if "user_id" not in request.session: #make sure logged in
        return redirect("/")
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
            "travelPlan" : Travel.objects.all(),
            "yourTrips" : Travel.objects.filter(join = User.objects.get(id=request.session['user_id'])),
            "otherTrips" : Travel.objects.exclude(join = User.objects.get(id=request.session['user_id'])),
        }
        return render(request, "dashboard.html", context)

def addtrip(request):
    
    return render(request, "addtrip.html")

def create_trip(request):
    print("$" *100)
    print(request.POST)
    print("$" *100)
    errors = Travel.objects.travel_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/addtrip")
    newTrip = Travel.objects.create(
        destination = request.POST['travelDestination'],
        description = request.POST['travelDescription'],
        start_date = request.POST['startTravel'],
        enddate = request.POST['endTravel'],
        creator = User.objects.get(id=request.session['user_id'])
    )

    return redirect("/dashboard")

def tripInfo(request, travel_id):
    context = {
        "travelInfo" : Travel.objects.get(id=travel_id),
        "user" : User.objects.get(id=request.session['user_id']),
    }

    return render(request, "viewTrip.html", context)

def joinTrip(request, travel_id):
    #get user to join
    loggedInUser = User.objects.get(id=request.session['user_id'])
    #get travel to join
    travel = Travel.objects.get(id=travel_id)
    #make the join
    travel.join.add(loggedInUser)

    return redirect("/dashboard")

def cancelTrip(request, travel_id):
    #get user to join
    loggedInUser = User.objects.get(id=request.session['user_id'])
    #get travel to join
    travel = Travel.objects.get(id=travel_id)
    #make the join
    travel.join.remove(loggedInUser)

    return redirect("/dashboard")

def delete(request, travel_id):
    travelToDelete = Travel.objects.get(id= travel_id)
    travelToDelete.delete()

    return redirect("/dashboard")