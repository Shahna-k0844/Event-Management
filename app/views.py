from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, login 
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from .models import *
from .forms import *

# Create your views here.

def homefunction(request):
    if request.user.is_superuser:
        return redirect('adminhome')
    else:
        return render(request,'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # messages.success(request, "Account created successfully")

            # Redirect to a different page after successful signup, like 'home' or the previous page
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return render(request, 'signup.html')
    
    

def loginfunction(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Get the next URL or redirect to home
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('home')
            if user.is_superuser:
                return redirect('adminhome')
            else:
                return redirect(next_url)
        else:
            messages.error(request,'invalid username or password')
            # return redirect('login')

        # If authentication fails, redirect back to the previous page or home
        return redirect(request.META.get('HTTP_REFERER') or 'home')
    
    return redirect('home')

def logoutfunction(request):
    logout(request)
    return redirect('home')        
                
def adminhome(request):
    if request.user.is_superuser:
        event=Event.objects.all()
        book=BookEvent.objects.all()
        return render(request,'adminhome.html',{'event':event,'book':book})
    else:
        return redirect('home')
      
def bookingview(request):
    if request.user.is_superuser:
        book=BookEvent.objects.all()
        return render(request,'bookingview.html',{'book':book})
    else:
        return redirect('home')
    # return render(request,'adminhome.html')
def enquery_admin(request):
    if request.user.is_superuser:
        enquery=Enquiery.objects.all()
        return render(request,'enquery.html',{'enquery':enquery})
    else:
        return redirect('home')
def createEvent(request):
    if request.user.is_superuser:
        if request.method=='POST':
            form=CreateEvent(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('adminhome')
        else:
            form=CreateEvent() 
        return render(request,'create_event.html',{'form':form}) 
    else:
        return redirect('home')
     

def bookdetails(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event =Event.objects.get(id=event_id)
        booking = BookEvent.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            description=request.POST['description'],
            date=request.POST['date'],
            place=request.POST['place'],
            event=event,
            user=request.user,
        )
        booking.save()
        messages.success(request, "Event booked successfully!")
        return redirect('eventview' )

    # return redirect('eventview') 
def enquiery(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        description=request.POST['description']
        event=request.POST['event']
        client=Enquiery.objects.create(name=name,email=email,phone=phone,event=event,description=description)
        client.save()
        return redirect('home')

def deletefunction(request,id):
    event=Event.objects.get(id=id)
    event.delete()
    return redirect('adminhome')
def editfunction(request,id):
    edit=Event.objects.get(id=id)
    form=CreateEvent(request.FILES,request.POST)
    if request.method=='POST':
        if edit:
            edit.name=request.POST['name']
            if 'image' in request.FILES: 
                edit.image=request.FILES['image']
            edit.description=request.POST['description']
            edit.save()
        return redirect('adminhome')
    else:
        form=CreateEvent() 
               
    return render(request,'editevent.html',{'edit':edit,'form':form})
def eventview(request):
    events = Event.objects.all()
    if request.user.is_authenticated:
        for event in events:
            event.booked = event.is_booked_by_user(request.user)  # Mark as booked if user has booked this event
    else:
        for event in events:
            event.booked = False  # Mark all events as not booked if user is not logged in

    return render(request, 'eventview.html', {'event': events})
def logintobook(request):
    return render(request,'logintobook.html')
def booked(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        today = timezone.now().date()  

        return render(request, 'booked.html', {'event': event,'min_date': today})
    else:
        return render(request,'logintobook.html')


def view_details(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.filter(id=event_id).first()
        
        if event:
            booking = BookEvent.objects.filter(event=event, user=request.user).first()
            
            if booking:
                return render(request, 'view_details.html', {'booking': booking, 'event': event})
            # else:
            #     return render(request, 'no_booking.html', {'event': event})  
        # else:
        #     return render(request, 'event_not_found.html') 
    else:
        return redirect('login')


def cancel_booking(request,event_id):
    if request.user.is_authenticated:
        event=Event.objects.all()
        booking = BookEvent.objects.filter(event__id=event_id, user=request.user)
        if booking.exists():
            booking.delete()  
        
        return redirect('eventview')  

    
def aboutfunction(request):
    return render(request,'about.html')

def download_file(request, file):
    # Define the file path using MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, file)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404("File does not exist")

    # Open the file for reading its bytes
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file}"'
        return response
def gallery(request):
    images=MainImage.objects.all()
    return render(request,'gallery.html',{'images':images})
def subgallery(request,id):
    image=SubImage.objects.filter(images=id)
    return render(request,'subgallery.html',{'subimage':image})
def create_main_image(request):
    if request.user.is_superuser:
        if request.method=='POST':
            form=create_main(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('adminhome')
        else:
            form=create_main()
    else:
        return redirect('loginpage')
    return render(request,'create_mainimage.html',{'forms':form})
def create_sub_image(request):
    if request.user.is_superuser:
        if request.method=='POST':
            form=create_sub(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('adminhome')
        else:
            form=create_sub()
    else:
        return redirect('loginpage')
    return render(request,'create_subimage.html',{'forms':form})