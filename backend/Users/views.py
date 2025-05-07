from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login


def Login(request) : 
    if request.method == 'POST'  : 
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is None : 
            error_message = "identifiants incorrects !"
            return render(request , "Users/Login.html", {'error_message' : error_message})
        else  : 
            login(request,user)
            
            if user.is_superuser : 
                return redirect('/admin/') #Rediriger l'utilisateur vers l'interface d'administration
              
            return HttpResponse("Identifiants corrects !")
    
    return render(request, 'Users/Login.html' , {})
