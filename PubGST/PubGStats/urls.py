from django.urls import path
from PubGStats import views

urlpatterns = [
    path('damage_trend/', views.run_script_view, name='damage_trend'),
    path('kills_assists_dbnos/', views.run_script_view, name='kills_assists_dbnos'),
    path('addplayers/', views.addplayers, name='addplayers'),
    path('results/', views.run_script_view, name='results'),
]
