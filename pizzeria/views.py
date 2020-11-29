from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from .models import Customer, Order, Size, Topping, OrderItem
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderItemForOrderSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

# @api_view(["GET", "POST"])
# def order_list(request):
#     if request.method == "GET":
#         orders = Order.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = OrderSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ViewSet):
    """ ViewSet to handle pizza orders """

    def list(self, request):
        """To fetch all the orders in database, filters on the basis of status

        Args:
            request (request): django request object

        Returns:
            Response: List of all orders
        """
        status = request.GET.get("status")
        delivered = request.GET.get("delivered")

        if status:
            orders = Order.objects.filter(status=status)
        else:
            orders = Order.objects.filter(
                Q(status="pending") | Q(status="ready") | Q(status="dispatched")
            )

        if delivered == "True" or delivered == "true":
            orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new order in database

        Args:
            request (request): django request object

        Returns:
            Response: Details of created order
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Fetches order details from database with given pk

        Args:
            request (request): django request object
            pk (int) : Primary Key (id) of the order

        Returns:
            Response: Details of created order
        """
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Updates order details in database with given pk

        Args:
            request (request): django request object
            pk (int) : Primary Key (id) of the order

        Returns:
            Response: Details of updated order
        """
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        print("deleting...")
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_200_OK)


class OrderItemForItemViewSet(viewsets.ViewSet):
    """Viewset to handle order items for a specific order"""

    def list(self, request, pk=None):
        """Fetches order items from database with given order id

        Args:
            request (request): django request object
            pk (int) : Primary Key (id) of the order

        Returns:
            Response: List of order items for the order
        """
        all_items = OrderItem.objects.all()
        items = all_items.filter(order__id=pk)

        serializer = OrderItemForOrderSerializer(items, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ViewSet):
    """Viewset to manage order items"""

    def list(self, request):
        """Fetches list of all order items

        Args:
            request (request): django request object

        Returns:
            Response: List of order items
        """
        all_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(all_items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Fetches order item details from database with given pk

        Args:
            request (request): django request object
            pk (int) : Primary Key (id) of the order item

        Returns:
            Response: Details of order item
        """
        queryset = OrderItem.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderItemSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        """Creates new order item

        Args:
            request (request): django request object

        Returns:
            Response: Details of created order item
        """
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Updates the order item with given pk

        Args:
            request (request): django request object
            pk (int) : Primary Key (id) of the order item

        Returns:
            Response: Details of updated order item
        """
        item = get_object_or_404(OrderItem, pk=pk)
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
