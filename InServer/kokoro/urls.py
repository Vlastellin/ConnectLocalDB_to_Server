from django.conf.urls import url
from django.urls import path, include
from .views import *
urlpatterns = [
    path('connect_to_server/mens/', Connect_mens.as_view()),
    path('connect_to_server/object/', Connect_object.as_view()),
    path('connect_to_server/task_section/', Connect_task_section.as_view()),
    path('connect_to_server/task/', Connect_task.as_view()),
    path('connect_to_server/employee/', Connect_employee.as_view()),
    path('connect_to_server/plan/', Connect_plan.as_view()),
    path('connect_to_server/operation/', Connect_operation.as_view()),
    path('connect_to_server/accept/', Connect_accept.as_view()),
    path('connect_to_server/pass/', Connect_pass.as_view()),
    path('connect_to_server/update/', Update.as_view()),
    #path(r'^app/take_task/([0-9]*)/$', Take_task.as_view()),
    url(r'^app/take_task/([0-9]*)/$', take_task, name="take_task"),
    url(r'^app/([0-9]*)/$', login, name='login'),
    url(r'^app/tasks/([0-9]*)/$', get_task, name='get_task'),
    url(r'^app/operations/([0-9]*)/$', get_operation, name='get_operation'),
    url(r'^app/operations/([0-9]*)/([0-9]*)/$', pass_operation, name='pass_operation')
    
]