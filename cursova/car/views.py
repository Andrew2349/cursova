from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from fontTools.misc.arrayTools import quantizeRect

from car.decorator import admin_required
from car.email import send_email, send_order_details
from car.forms import CarForm, SupplierForm, OrderForm
from car.models import Car, Supplier, Order


class CarListView(ListView):
    model = Car
    template_name = "catalog.html"
    context_object_name = "cars"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = get_brands()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        min = self.request.GET.get('min')
        max = self.request.GET.get('max')
        brand = self.request.GET.get('brand')
        model = self.request.GET.get('model')
        if min:
            queryset = queryset.filter(price__gte=min)
        if max:
            queryset = queryset.filter(price__lte=max)
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        if model:
            queryset = queryset.filter(model__icontains=model)
        return queryset

class UserCarListView(ListView):
    model = Order
    template_name = "account.html"
    context_object_name = "orders"
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(custom_user=user)

        #виймати з запиту який користувач його відправив і знайти для цього користувача всі його замовлення, і отримати з замовлень всі машини які він купив
class OrderListView(ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['brands'] = get_brands()
        context['customers'] = get_purchasers()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.GET.get('brand')
        customer = self.request.GET.get('customer')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        if brand:
            queryset = queryset.filter(car__brand__icontains=brand)
        if customer:
            queryset = queryset.filter(custom_user__fullname__icontains=customer)
        if from_date:
            date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(date__gte=date_obj)
        if to_date:
            date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            date_obj = date_obj.replace(hour=23, minute=59, second=59, microsecond=0)
            queryset = queryset.filter(date__lte=date_obj)
        return queryset.order_by('-date')

@admin_required
def car_form(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'car_form.html', {'form': form})
    if request.method == "GET":
        form = CarForm()
        return render(request, 'car_form.html', {'form': form})
    return redirect('/404')
@admin_required
def update_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'car_form.html', {'form': form})
    if request.method == "GET":
        form = CarForm(instance=car)
        return render(request, 'car_form.html', {'form': form})
    return redirect('/404')

@admin_required
def update_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/admin/orders/')
        return render(request, 'order_form.html', {'form': form})
    if request.method == "GET":
        form = OrderForm(instance=order)
        return render(request, 'order_form.html', {'form': form})
    return redirect('/404')

@admin_required
def supplier_form(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'supplier_form.html', {'form': form})
    if request.method == "GET":
        form = SupplierForm()
        return render(request, 'supplier_form.html', {'form': form})
    return redirect('/404')

@admin_required
def update_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'supplier_form.html', {'form': form})
    if request.method == "GET":
        form = SupplierForm(instance=supplier)
        return render(request, 'supplier_form.html', {'form': form})
    return redirect('/404')
@admin_required
def delete_car(request, car_id):

    car = get_object_or_404(Car, pk=car_id)
    if request.method == "POST":
        car.delete()
    return redirect('/catalog/')

def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.delete()
    return redirect('/admin/orders/')

def purchase_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'purchase_page.html', {'car': car})

def get_brands():
    brands = Car.objects.values_list('brand').distinct()
    return [brand[0] for brand in brands]

def get_purchasers():
    purchasers = Order.objects.values_list('custom_user__fullname').distinct()
    return [purchaser[0] for purchaser in purchasers]




@login_required
def make_order(request, car_id):
    if request.method == "POST":
        car = get_object_or_404(Car, id=car_id)
        custom_user = request.user
        order = Order.objects.create(custom_user=custom_user, car=car, price=car.final_price())
        send_order_details(order)
        return redirect(f'/order/details/{order.id}')
    return redirect('/404')
@login_required
def order_detail(request, order_id):
    if request.method == "GET":
        order = get_object_or_404(Order, pk=order_id)
        return render(request, "order.html", {'order': order})

@login_required
def update_profile_image(request):
    if request.method == 'POST' and 'profile_image' in request.FILES:
        user = request.user
        user.profile_image = request.FILES['profile_image']
        user.save()
        return redirect('/account/')
    return redirect('/account/')
