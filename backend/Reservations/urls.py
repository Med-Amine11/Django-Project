from django.urls import path
from .views import effectuer_reservation, mes_reservations, annuler_reservation, modifier_reservation

urlpatterns = [
    path('Salle-<int:salle_id>', effectuer_reservation, name='effectuer_reservation'),
    path('mes-reservations/', mes_reservations, name='mes_reservations'),
    path('annuler/<int:reservation_id>/', annuler_reservation, name='annuler_reservation'),
    path('modifier/<int:reservation_id>/', modifier_reservation, name='modifier_reservation'),
]