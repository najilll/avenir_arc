from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.index,               name='index'),
    path('api/projects/',                  views.api_projects,        name='api_projects'),
    path('api/projects/<slug:slug>/',      views.api_project_detail,  name='api_project_detail'),
    path('api/categories/',                views.api_categories,      name='api_categories'),
    path('api/stats/',                     views.api_stats,           name='api_stats'),
    path('api/model3d/',                   views.api_active_3d,       name='api_active_3d'),
    path('api/enquiry/',                   views.api_submit_enquiry,  name='api_enquiry'),
]
