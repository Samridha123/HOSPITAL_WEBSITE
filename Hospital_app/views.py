from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BookingForm
from .models import Departments, Doctors

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'confirmation.html')
    form = BookingForm()
    dict_form = {
        'form': form
    }
    return render(request, 'booking.html', dict_form)

def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, 'doctors.html', dict_docs)

def contact(request):
    return render(request, 'contact.html')

def department(request):
    dict_dept={
        'dept': Departments.objects.all()
    }
    return render(request, 'department.html', dict_dept)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid username or password")
            return redirect("login")
    return render(request, "login.html")

def register(request, turn=None):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect("register")
            else:
                user=User.objects.create_user(username=username,email=email,password=password)


                user.save()
                return redirect('login')

        else:
            messages.info(request,"passwords do not match")
            return redirect("register")

        return redirect('/')

    return render(request,"register.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

