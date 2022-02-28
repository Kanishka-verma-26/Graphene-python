from rest_framework import serializers

from .models import Product

""" DRF Mutation Serializer """

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id","category",'slug',"title","description","regular_price","discount_price"]               # in fields we define data that we want to collect


