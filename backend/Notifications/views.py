from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def mes_notifications(request):
    # On récupère les notifications de l'utilisateur connecté, les plus récentes d'abord
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_envoi')

    # On les passe au template pour affichage
    return render(request, 'Notifications/liste.html', {
        'notifications': notifications
    })
