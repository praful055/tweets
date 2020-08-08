from django.urls import path

from Student import views

app_name = 'Student'

urlpatterns = [
    path('', views.show_graph, name='show_graph'),
    path('fetch_sensor_values_ajax', views.fetch_sensor_values_ajax, name='fetch_sensor_values_ajax'),

]