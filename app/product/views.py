from core.models import Product
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from core.models import Product, Order
from product import serializers

from django.http import HttpResponse

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
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
class ProductViewSet(BaseRecipeAttrViewSet):

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


