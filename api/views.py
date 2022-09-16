import stripe
from django.conf import settings
from django.db.models import Sum
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Item, Order


class ItemDetail(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    queryset = Item.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({
            'item': self.object,
            'stipe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        },
            template_name='item_info.html')


class OrderDetail(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    queryset = Order.objects.all().annotate(total_price=Sum('item__price'))
    renderer_classes = [TemplateHTMLRenderer]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({
            'total_price': self.object.total_price,
            'order': self.object,
            'items': self.object.item.all(),
            'stipe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        },
            template_name='order_info.html')


@api_view(['GET'])
def create_session_for_item(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order = Item.objects.get(id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Оплата товара {order.name}',
                },
                'unit_amount': int(order.price) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('success/'),
        cancel_url=request.build_absolute_uri('cancelled/')
    )

    return Response({"session_id": session.id})


@api_view(['GET'])
def create_session_for_order(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order = Order.objects. \
        annotate(total_price=Sum('item__price')). \
        get(id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Оплата заказа № {order.id}',
                },
                'unit_amount': int(order.total_price) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('success/'),
        cancel_url=request.build_absolute_uri('cancelled/')
    )

    return Response({"session_id": session.id})


class CancelledView(TemplateView):
    template_name = 'cancel.html'


class SuccessView(TemplateView):
    template_name = 'success.html'