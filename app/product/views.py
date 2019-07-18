from core.models import Product
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from core.models import Product, Order
from product import serializers

from django.http import HttpResponse

class BaseOrderAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(order__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Create your views here.
class ProductViewSet(BaseOrderAttrViewSet):

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_integers(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        products = self.request.query_params.get('products')
        queryset = self.queryset
        if products:
            product_ids = self._params_to_integers(products)
            queryset = queryset.filter(producttags__id__in=product_ids)

        return queryset.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




