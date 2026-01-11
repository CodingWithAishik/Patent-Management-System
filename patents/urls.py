from django.urls import path
from . import views

app_name = 'patents'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Copyright URLs
    path('copyrights/', views.copyright_list, name='copyright_list'),
    path('copyrights/search/', views.copyright_search, name='copyright_search'),
    path('copyrights/create/', views.copyright_create, name='copyright_create'),
    path('copyrights/<int:pk>/update/', views.copyright_update, name='copyright_update'),
    path('copyrights/<int:pk>/delete/', views.copyright_delete, name='copyright_delete'),
    
    # Patent Filed URLs
    path('patents/filed/', views.filed_list, name='filed_list'),
    path('patents/filed/search/', views.filed_search, name='filed_search'),
    path('patents/filed/create/', views.filed_create, name='filed_create'),
    path('patents/filed/<int:pk>/update/', views.filed_update, name='filed_update'),
    path('patents/filed/<int:pk>/delete/', views.filed_delete, name='filed_delete'),
    
    # Patent Granted URLs
    path('patents/granted/', views.granted_list, name='granted_list'),
    path('patents/granted/search/', views.granted_search, name='granted_search'),
    path('patents/granted/create/', views.granted_create, name='granted_create'),
    path('patents/granted/<int:pk>/update/', views.granted_update, name='granted_update'),
    path('patents/granted/<int:pk>/delete/', views.granted_delete, name='granted_delete'),
    
    # IP Category Management URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Dynamic IP URLs
    path('ip/<slug:category_slug>/', views.ip_list, name='ip_list'),
    path('ip/<slug:category_slug>/search/', views.ip_search, name='ip_search'),
    path('ip/<slug:category_slug>/create/', views.ip_create, name='ip_create'),
    path('ip/<slug:category_slug>/<int:pk>/edit/', views.ip_edit, name='ip_edit'),
    path('ip/<slug:category_slug>/<int:pk>/delete/', views.ip_delete, name='ip_delete'),
]
