from rest_framework import serializers
from .models import Customer, Order, Size, OrderItem, Topping
from rest_framework.exceptions import bad_request, NotFound
from utils.errors import NotFoundExcpetion


class SizeSerializer(serializers.ModelSerializer):
    """ Serializer for Pizza Size """

    id = serializers.IntegerField()

    class Meta:
        model = Size
        fields = ("id", "name", "price")


class ToppingSerializer(serializers.ModelSerializer):
    """ Serializer for Pizza Topping """

    id = serializers.IntegerField()

    class Meta:
        model = Topping
        fields = ("id", "name", "price")


class CustomerSerializer(serializers.ModelSerializer):
    """ Serializer for Customer """

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = ("id", "name", "number", "address")


class OrderItemSerializer(serializers.ModelSerializer):
    """ Serializer for General Order Item """

    size = SizeSerializer()
    topping = ToppingSerializer()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ("id", "order", "size", "topping", "quantity", "notes")

    def create(self, validated_data):
        """Creates a new order item in database

        Args:
            validated_data (dict): validated data from the request

        Raises:
            serializers.ValidationError: If size is not available
            serializers.ValidationError: If topping is not available

        Returns:
            Order Item: Details of the order item that was created
        """
        topping = validated_data.pop("topping")
        size = validated_data.pop("size")

        # try:
        #     order = Order.objects.get(pk=order_id)
        # except Order.DoesNotExist:
        #     raise serializers.ValidationError("Topping does not exist")

        try:
            topping = Topping.objects.get(pk=topping.get("id"))
        except Topping.DoesNotExist:
            raise serializers.ValidationError("Topping does not exist")

        try:
            size = Size.objects.get(pk=size.get("id"))
        except Size.DoesNotExist:
            raise serializers.ValidationError("Size does not exist")

        order_item = OrderItem.objects.create(
            topping=topping, size=size, **validated_data
        )

        return order_item

    def update(self, instance, validated_data):
        """Updates a order item in database with given id

        Args:
            instance (order object): Instance of the order that needs to be updated
            validated_data (dict): validated data from the request

        Raises:
            serializers.ValidationError: If size is not available
            serializers.ValidationError: If topping is not available

        Returns:
            Order Item: Details of the order item that was updated
        """
        topping = validated_data.pop("topping")
        size = validated_data.pop("size")

        # try:
        #     order = Order.objects.get(pk=order_id)
        # except Order.DoesNotExist:
        #     raise serializers.ValidationError("Topping does not exist")

        try:
            topping = Topping.objects.get(pk=topping.get("id"))
        except Topping.DoesNotExist:
            raise serializers.ValidationError("Topping does not exist")

        try:
            size = Size.objects.get(pk=size.get("id"))
        except Size.DoesNotExist:
            raise serializers.ValidationError("Size does not exist")

        order_item = OrderItem.objects.create(
            topping=topping, size=size, **validated_data
        )

        instance.order = validated_data.get("order", instance.order)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.topping = topping
        instance.size = size
        instance.save()
        return instance


class OrderItemForOrderSerializer(serializers.ModelSerializer):
    """ Serializer for order items for a partiular order """

    size = SizeSerializer()
    topping = ToppingSerializer()
    id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ("id", "size", "topping", "quantity", "notes")


class OrderSerializer(serializers.ModelSerializer):
    """ Order serializer """

    customer = CustomerSerializer()
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        depth = 1
        fields = (
            "id",
            "customer",
            "status",
            "items",
        )

    def create(self, validated_data):
        """Creates a new order in database

        Args:
            validated_data (dict): validated data from the request

        Raises:
            serializers.ValidationError: If size is not available
            serializers.ValidationError: If topping is not available

        Returns:
            Order: Details of the order that was created
        """
        customer = validated_data.pop("customer")
        if not customer.get("id"):
            customer = Customer.objects.create(**customer)
        else:
            try:
                customer = Customer.objects.get(pk=customer.get("id"))
            except Customer.DoesNotExist:
                customer.pop("id")
                customer = Customer.objects.create(**customer)

        order = Order.objects.create(customer=customer, **validated_data)

        return order

    def update(self, instance, validated_data):
        """Creates a new order in database

        Args:
            validated_data (dict): validated data from the request

        Returns:
            Order Item: Details of the order that was updated
        """
        customer = validated_data.pop("customer")
        if not customer.get("id"):
            customer = Customer.objects.create(**customer)
        else:
            try:
                customer = Customer.objects.get(pk=customer.get("id"))
            except Customer.DoesNotExist:
                customer.pop("id")
                customer = Customer.objects.create(**customer)

        instance.status = validated_data.get("status", instance.status)
        instance.customer = customer
        instance.save()
        return instance