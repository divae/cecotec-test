from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import csv
from io import StringIO
from core.models import Order, Product
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail, EmailMessage

from product import serializers


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

        #send_email(request)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


def send_email(request):
    subject = request.POST.get('subject', 'request.order.name')
    message = request.POST.get('message', 'message')
    from_email = request.POST.get('from_email', 'order.user.mail')
    if subject and message and from_email:
        try:
            assigned_order = order.objects.filter(user=request.user)
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            for order in assigned_order:
                csvwriter.writerow([order.name, order.products])
            message = EmailMessage("Hello", "Your Leads", "myemail@gmail.com", ["myemail@gmail.com"])
            message.attach('invoice.csv', csvfile.getvalue(), 'text/csv')
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
