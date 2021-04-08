from django.urls import path
from AgentServer import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout, name='logout'),
    path('api/poststory/', views.post, name='poststory'),
    path('api/getstories/', views.get_story, name='get'),
    path('api/deletestory/', views.delete, name='deletestory'),

]
