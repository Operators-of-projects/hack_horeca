from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance')


@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'vendor', "cost", "get_products", "status")

    def get_products(self, obj):
        return ",".join([d.name for d in obj.product.all()])

    get_products.short_description = "Продукты"


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'score')
