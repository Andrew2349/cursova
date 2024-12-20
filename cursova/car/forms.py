from django import forms

from car.models import Car, Supplier, Order


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['supplier', 'brand', 'model', 'body_type', 'fuel_type','engine_capacity','color',
                  'year', 'price', 'mileage', 'available', 'img', 'discount']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'cars', 'details']

class OrderForm(forms.ModelForm):
    car_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    supplier_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'readonly':'readonly'}))
    purchaser_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    status = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('Pending', 'Pending'),
                                                                    ('Confirmed', 'Confirmed'),
                                                                    ('Preparing for delivery', 'Preparing for delivery'),
                                                                    ('Delivered', 'Delivered'),
                                                                    ('Canceled', 'Canceled')])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_name'].initial=self.instance.car.brand + '-' + self.instance.car.model
        self.fields['supplier_name'].initial=self.instance.car.supplier.name
        self.fields['purchaser_name'].initial=self.instance.custom_user.fullname

    class Meta:
        model = Order
        fields = ['car_name','supplier_name','date','purchaser_name', 'status']