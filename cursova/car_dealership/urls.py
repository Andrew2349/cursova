"""
URL configuration for car_dealership project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from car import views as car
from auth_user import views as auth
from car_dealership.views import index, account
from car_dealership.views import about, forbidden, not_found

urlpatterns = [
    path('catalog/', car.CarListView.as_view(), name='catalog'),
    path('register/', auth.register_view),
    path('logout/', auth.logout_view),
    path('', index),

    path('', include('django.contrib.auth.urls')),
    path('admin/car/', car.car_form),
    path('admin/car/<str:car_id>', car.update_car),
    path('admin/supplier/', car.supplier_form),
    path('admin/supplier/<int:supplier_id>', car.update_supplier),
    path('about/', about, name='about'),
    path('catalog/purchase/car/<str:car_id>', car.purchase_car, name='purchasing'),
    path('admin/car/<str:car_id>/delete/', car.delete_car, name='delete'),

    path('order/<str:car_id>', car.make_order, name='order'),
    path('order/details/<int:order_id>', car.order_detail, name='order_detail'),
    path('admin/orders/', car.OrderListView.as_view(), name='orders'),
    path('admin/orders/<int:order_id>', car.update_order, name='update_order'),
    path('admin/orders/delete/<int:order_id>/', car.delete_order, name='delete_order'),

    path('403/', forbidden, name='forbidden'),
    path('404/', not_found, name='not_found'),
    path('account/', car.UserCarListView.as_view(), name='account'),
    path('update-image/', car.update_profile_image, name='update_profile_image')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

