from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login , logout


def Login(request) : 
    
    if request.user.is_authenticated:
        return redirect('Consultation_salles') 
    
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
              
            return redirect('Consultation_salles')
    
    return render(request, 'Users/Login.html' , {})


def deconnexion(request):
    logout(request)  # supprime l'utilisateur de la session
    return redirect('login')  # ou vers une page d'accueil
