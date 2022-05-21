from rest_framework import serializers

from .models import Client, Product, Vendor, Transaction


class AddClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('name', )


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = '__all__'


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('vendor', 'name', 'status', 'price')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'vendor', 'status', 'price')


# class ProductTransSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', )


class VendorTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('status', 'cost', 'response', 'client', 'product')


class ClientTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('status', 'cost', 'response', 'vendor', 'product')


class DetailTransaction(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
