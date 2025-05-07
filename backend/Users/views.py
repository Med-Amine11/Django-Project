from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate


def Login(request) : 
    if request.method == 'POST'  : 
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is None : 
            error_message = "identifiants incorrects !"
            return render(request , "Users/Login.html", {'error_message' : error_message})
        else  : 
            return HttpResponse("Identifiants corrects !")
    
    return render(request, 'Users/Login.html' , {})
