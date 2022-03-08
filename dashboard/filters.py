"""filters the product for customer"""
import django_filters
from django_filters import RangeFilter

from product.models import Product

class ProductFilter(django_filters.FilterSet):
    """custom filter"""
    price = RangeFilter()

    class Meta:
        """meta attributes for this filter"""
        model = Product
        fields = '__all__'
        exclude = ['image','quantity' , 'description']

class SalesFilter(django_filters.FilterSet):
    """custom filter"""

    class Meta:
        """meta attributes for this filter"""
        model = Product
        fields = '__all__'
        exclude = ['image','quantity', 'description', 'price', 'name', 'company', 'soldcount', 'provider', 'material', 'rating', 'color']

