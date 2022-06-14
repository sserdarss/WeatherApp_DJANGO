from django.shortcuts import render, redirect
from decouple import config
import requests
from pprint import pprint
from .models import City
from django.contrib import messages
from django.shortcuts import get_object_or_404




def home(request):

    # u_city = 'Amsterdam'
    API_key = config('API_KEY')
    u_city = request.GET.get('name')
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_key}&units=metric"
        response = requests.get(url)
        if response.ok:
            content = response.json()
            r_city = content['name']
            if City.objects.filter(name=r_city):
                messages.warning(request, 'City already exists!')
            else:
                City.objects.create(name=r_city)
                messages.success(request, 'City created!')
        else:
            messages.error(request, 'There is no city!')



    cities= City.objects.all()
    city_data = []
   
    
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'

        r = requests.get(url)
        content = r.json()
    
        data = {
            'city': city,
            'temp': content['main']['temp'],
            'icon' : content['weather'][0]['icon'],
            'desc' : content['weather'][0]['description'],
        }
        city_data.append(data)

    context = {
            'city_data': city_data,
            } 
    
    
    return render(request,"weatherapp/home.html",context)


def delete(request, id):
        city = get_object_or_404(City, id=id)
        city.delete()
        messages.success(request, 'City successfully deleted!')
        return redirect('home')
