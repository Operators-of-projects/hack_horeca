from geopy import distance
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Client, Vendor, Transaction, Report
from .serializers import VendorSerializer, ProductSerializer, ClientSerializer, ClientTransactionSerializer, DetailTransaction, VendorTransactionSerializer


class AddClientView(APIView):

    def post(self, request):
        client = Client.objects.create(name=request.data.get('name'))
        return Response({'id': client.pk}, status=status.HTTP_201_CREATED)


class DetailClientView(APIView):

    def get(self, request, client_id):
        client = Client.objects.get(pk=client_id)
        ser = ClientSerializer(client)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, client_id):
        client = Client.objects.get(pk=client_id)
        client.balance = request.data.get('balance') if request.data.get('balance') else client.balance
        # TODO: пересчет рейинга???????
        client.rating = request.data.get('rating') if request.data.get('rating') else client.rating
        client.lat = request.data.get('lat') if request.data.get('lat') else client.lat
        client.long = request.data.get('long') if request.data.get('long') else client.long
        client.save()
        return Response({'id': client.pk}, status=status.HTTP_200_OK)


class AddVendorView(APIView):

    def post(self, request):
        vendor = Vendor.objects.create(name=request.data.get('name'))
        return Response({'id': vendor.pk}, status=status.HTTP_201_CREATED)


class DetailVendorView(APIView):

    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        ser = ClientSerializer(vendor)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.balance = request.data.get('balance') if request.data.get('balance') else vendor.balance
        vendor.rating = request.data.get('rating') if request.data.get('rating') else vendor.balance
        vendor.status = request.data.get('status') if request.data.get('status') else vendor.balance
        vendor.lat = request.data.get('lat') if request.data.get('lat') else vendor.lat
        vendor.long = request.data.get('long') if request.data.get('long') else vendor.long
        vendor.save()
        return Response({'id': vendor.pk}, status=status.HTTP_200_OK)


class GetVendersView(APIView):
    def get(self, request):
        venders = Vendor.objects.all()
        ser = VendorSerializer(venders, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class CreateProductView(APIView):

    def post(self, request):
        product = Product.objects.create(**request.data)
        return Response({'id': product.pk}, status=status.HTTP_201_CREATED)


def get_product_by_id(product_id):
    try:
        return Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404


class DetailProductView(APIView):

    def get(self, request, product_id):
        product = get_product_by_id(product_id)
        context = {
            'id': product.id,
            'name': product.name,
            'vendor': product.vendor.pk,
            'status': product.status,
            'price': product.price,
        }
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        product = get_product_by_id(product_id)
        product.name = request.data.get('name')
        product.status = request.data.get('status')
        product.price = request.data.get('price')
        product.save()
        return Response({'id': product.id}, status=status.HTTP_202_ACCEPTED)


class ProductsView(APIView):

    def get(self, request, vendor_id):
        products = Product.objects.filter(vendor=vendor_id)
        ser = ProductSerializer(products, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AddTransaction(APIView):
    """
    {
        "vendor_id": 1,
        "products": [1, 2],
        "client_id": 2
    }
    """
    def post(self, request):

        vendor = Vendor.objects.get(id=request.data.get("vendor_id"))
        products = Product.objects.filter(id__in=request.data.get("products"))
        cost = 0
        for product in products:
            cost += product.price
        if request.data.get("client_id"):
            client = Client.objects.get(id=request.data.get("client_id"))
            new_transaction = Transaction.objects.create(vendor=vendor, client=client, cost=cost)
        else:
            new_transaction = Transaction.objects.create(vendor=vendor, cost=cost)
        new_transaction.product.add(*products)
        resp = {"trasaction_id": new_transaction.pk}
        return Response(resp)


class TransactionToDone(APIView):
    """
    {"transaction_id": 1}
    """
    def post(self, request):
        transaction_id = request.data.get("transaction_id")
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.client.balance = transaction.client.balance - transaction.cost
        transaction.vendor.balance = transaction.vendor.balance + transaction.cost
        transaction.client.save()
        transaction.vendor.save()
        Transaction.objects.filter(id=transaction_id).update(status=3)
        return Response({"result": True})


class TransactionToViewed(APIView):
    """
    {"transaction_id": 1,}
    """
    def post(self, request):
        transaction_id = request.data.get("transaction_id")
        Transaction.objects.filter(id=transaction_id).update(status=2)
        return Response({"result": True})


class VendorTransactionView(APIView):
    def get(self, request, vendor_id):
        transactions = Transaction.objects.filter(vendor=vendor_id)
        ser = VendorTransactionSerializer(transactions, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class ClientTransactionView(APIView):
    def get(self, request, client_id):
        transaction = Transaction.objects.filter(client=client_id)
        ser = ClientTransactionSerializer(transaction, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class DetailTransactionView(APIView):

    def get(self, request, transaction_id):
        tr = Transaction.objects.get(pk=transaction_id)
        ser = DetailTransaction(tr)
        return Response(ser.data, status=status.HTTP_200_OK)


class NewTransactionsView(APIView):
    def get(self, request, vendor_id):
        new_transactions = Transaction.objects.filter(vendor=vendor_id, status=1)
        ser = VendorTransactionSerializer(new_transactions)
        return Response(ser.data, status=status.HTTP_200_OK)


class AddReportToTransactionView(APIView):
    def post(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id)
        new_report = Report.objects.create(transaction=transaction, score=request.data.get('score'),
                                           comment=request.data.get('comment'))
        repost_scores = [r.score for r in Report.objects.filter(transaction__vendor__id=transaction.vendor.pk)]
        avg_score = sum(repost_scores) / len(repost_scores)
        transaction.vendor.rating = avg_score
        transaction.vendor.save()

        return Response({'id': new_report.pk}, status=status.HTTP_201_CREATED)


def on_beach(client, vendor):
    return distance.distance((client.lat, client.long), (vendor.lat, vendor.long)).km < 2


class GetClientsByGPSView(APIView):
    def get(self, request, vendor_id):
        """ ВСех чекать плохо - пробудь бизнес логику """
        vendor = Vendor.objects.get(pk=vendor_id)
        clients = [client for client in Client.objects.all() if on_beach(client, vendor)]
        ser = ClientSerializer(clients, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class GenerateQRView(APIView):
    def get(self, request):
        pass



# получить транзакции вендора/клиента/отдельная транзакция +
# писать репорты к транзакции +
# метод для мониторинга транзакции -> обычное получение транщакции??
# метод проверки, есть ли новые заказы -> возвращать первый +
