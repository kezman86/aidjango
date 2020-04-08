from django.urls import include, path
from . import views

urlpatterns = [
    path('getcases', views.getAllCases),
    path('case/<caseID>', views.viewCase),
    path('savecase', views.save_cases),
    path('cases', views.allcases, name = 'cases'),
    path('casedetail/<caseID>', views.casedetail, name = 'casedetail'),
    path('case/delete/<caseID>/', views.delete_case , name = 'delete_case' ),
]