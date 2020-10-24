from django.urls import path
from . import views

# from .views import SearchResultsView



urlpatterns = [
    path('', views.home, name='hotel-home'),
    path('tray/', views.tray, name='hotel-tray'),
    path('checkout/', views.checkout, name='hotel-checkout'),
    path('update_tray/', views.updateTray, name='update_tray'),
    path('search_results/', views.search_results, name='search_results'),
    path('process_order/', views.processOrder, name='process_order'),

]



