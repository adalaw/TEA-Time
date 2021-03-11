import django_filters
from django_filters import *
from django_filters.widgets import RangeWidget
from django.forms.widgets import *
from datetime import datetime, date

from .models import *

# views/manage_products
class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['code', 'price']


# views/manage_orders
class OrderFilter(django_filters.FilterSet):
    date_created = DateFromToRangeFilter(field_name='date_created', label='Date', widget=RangeWidget(attrs={'type': 'date'}))
    id = CharFilter(field_name='id', label='Order No.')

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            # status default = pending
            data.setdefault("status", 'Pending')
            # date filter default = today
            data.setdefault("date_created_min", date.today())
            data.setdefault("date_created_max", date.today())
        super(OrderFilter, self).__init__(data, *args, **kwargs)

    class Meta:
        model = Order
        fields = ['id', 'store', 'status', 'date_created', 'stay']


# views/report

class ReportFilter(django_filters.FilterSet):
    date_created = DateFromToRangeFilter(field_name='date_created', label='Date', widget=RangeWidget(attrs={'type': 'date'}))

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            # date filter default = today
            data.setdefault("date_created_min", date.today())
            data.setdefault("date_created_max", date.today())
        super(ReportFilter, self).__init__(data, *args, **kwargs)

    class Meta:
        model = Order
        fields = ['store', 'date_created']



