from django.shortcuts import render

import wikipedia as wk          #to fetch IP address's location and details about that location
from django.views.decorators.csrf import csrf_exempt
import requests
#by default it,using default parameters, it finds user's IP location automatically
#'me' represents, that it's user's IP address

def make_request(ip_address):
  if ip_address == 'me':
    response = requests.get('http://ipapi.co/json/')
  else:
    response = requests.get('http://ipapi.co/{}/json/'.format(ip_address))
  return response.json()

def find_ip_address(ips = 'me'):
    #try to return JSON of details regarding IP address
    return make_request(ips)

#function to generate link of wikipedia by fetching results from wikipedia
def get_url(keyword):
    links = wk.search(keyword)          #searching of keyword in wikipedia's website
    page = wk.page(links[0])                #taking 1st result
    return page.url


#http://maps.google.com/maps?q=24.197611,120.780512
'''for security purpose, I have moved API key to txt file and it is ignored in repository, if you wanna run this API,
you can get API key from google'''
API_KEY = open('key.txt','r').read()


#https://maps.google.com/?q=<lat>,<lng>
'''function to generate, URL of Map that would be embed in website, Expects parameters are latitude and longitude'''
def get_map_url(lat,lng):
    try:
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={lat},{lng}'
    except:
        return f'https://www.google.com/maps/embed/v1/place?key={API_KEY}&q='

'''index function to render template's html and data'''
@csrf_exempt
def index(request):
    if 'ip_address' in request.GET:            #fetching IP address from template
        data = find_ip_address(request.GET['ip_address'])  #if user enters data than it'll find it's IP details
    else:
        data = find_ip_address()    #if IP field is empty,it'll return user's address by default parameters
    try:
        # try to fetch URL for MAP using lat,lng fetched from IP
        map_url = get_map_url(data['latitude'], data['longitude'])
        page_link = get_url(f"{data['city']} in {data['country']}") #fetching wikipedia page link
    except :
        map_url = f'https://www.maps.google.com'
        page_link = 'https://www.wikipedia.org'
    return render(request,"index.html",{"data":data,'page_link':page_link,'map_url' : map_url}) #returning, template and dictionary to the templates