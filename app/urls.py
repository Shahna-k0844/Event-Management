from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.homefunction,name='home'),
    path('signup',views.signup,name='signup'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('logout',views.logoutfunction,name='logout'),
    path('login',views.loginfunction,name='login'),
    path('createevent',views.createEvent,name='createevent'),
    path('Bookevent',views.bookdetails,name='bookdetails'),
    path('enquiery',views.enquiery,name='enquiery'),
    path('booking',views.bookingview,name='booking'),
    path('delete<int:id>',views.deletefunction,name='delete'),
    path('edit<int:id>',views.editfunction,name='edit'),
    path('event',views.eventview,name='eventview'),
    path('booked<int:event_id>',views.booked,name='booked'),
    path('logintobook',views.logintobook,name='logintobook'),
    path('enquery_admin',views.enquery_admin,name='enquery_admin'),
    path('view_details<int:event_id>',views.view_details,name='view_details'),
    path('cancel_booking<int:event_id>',views.cancel_booking,name='cancel_event'),
    path('about',views.aboutfunction,name='about'),
    path('download/<str:file>/', views.download_file, name='download_file'),
    path('gallery',views.gallery,name='gallery'),
    path('sub_gallery<int:id>',views.subgallery,name='subgallery'),
    path('create_main_image',views.create_main_image,name='create_main_image'),
    path('create_sub_image',views.create_sub_image,name='create_sub_image'),

]