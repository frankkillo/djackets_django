from multiprocessing import context
import stripe

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import MyOrderSerializer, OrderSerializer


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='gbp',
                description='Charge to Djackets',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_price=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)