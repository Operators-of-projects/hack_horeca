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
        fields = ('vendor', 'name', 'status', 'price', 'img')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'vendor', 'status', 'price', 'img')


class ProductTransSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')


class VendorTransactionSerializer(serializers.ModelSerializer):
    product = ProductTransSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'status', 'cost', 'response', 'client', 'product', 'description', 'photo')


class ClientTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('status', 'cost', 'response', 'vendor', 'product')


class DetailTransaction(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
