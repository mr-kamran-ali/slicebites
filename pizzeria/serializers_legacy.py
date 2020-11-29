from rest_framework import serializers
from .models import Customer, Order, Size, OrderItem, Topping
from rest_framework.exceptions import bad_request, NotFound
from utils.errors import NotFoundExcpetion


class SizeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Size
        fields = ("id", "name", "price")


class ToppingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Topping
        fields = ("id", "name", "price")


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = ("id", "name", "number", "address")


class OrderItemSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    topping = ToppingSerializer()
    id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ("id", "size", "topping", "quantity", "notes")


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        depth = 1
        fields = (
            "id",
            "customer",
            "is_made",
            "is_dispatched",
            "is_collected",
            "is_delivered",
            "items",
        )

    def create(self, validated_data):
        customer = validated_data.pop("customer")
        if not customer.get("id"):
            customer = Customer.objects.create(**customer)
        else:
            try:
                customer = Customer.objects.get(pk=customer.get("id"))
            except Customer.DoesNotExist:
                customer.pop("id")
                customer = Customer.objects.create(**customer)

        order_items = validated_data.pop("items")
        order = Order.objects.create(customer=customer, **validated_data)

        for item in order_items:
            topping = item.pop("topping")
            try:
                topping = Topping.objects.get(pk=topping.get("id"))
            except Topping.DoesNotExist:
                raise serializers.ValidationError("Topping does not exist")

            size = item.pop("size")
            try:
                size = Size.objects.get(pk=size.get("id"))
            except Size.DoesNotExist:
                # data = {"error": "Bad Request (400)"}
                raise serializers.ValidationError("Size does not exist")

            OrderItem.objects.create(order=order, topping=topping, size=size, **item)
        return order

    def update(self, instance, validated_data):
        print(validated_data)
        customer = validated_data.pop("customer")
        if not customer.get("id"):
            customer = Customer.objects.create(**customer)
        else:
            try:
                customer = Customer.objects.get(pk=customer.get("id"))
            except Customer.DoesNotExist:
                customer.pop("id")
                customer = Customer.objects.create(**customer)

        # try:
        #     order_items = validated_data.pop("items")
        #     order_items = validated_data.pop("items")

        # except Customer.DoesNotExist:
        #     customer.pop("id")
        #     customer = Customer.objects.create(**customer)

        order_items = validated_data.pop("items")
        new_items = []
        if order_items:
            for item in order_items:
                order_item = OrderItem.objects.get(pk=item.get("id"))
                topping = item.pop("topping")
                try:
                    topping = Topping.objects.get(pk=topping.get("id"))
                except Topping.DoesNotExist:
                    raise serializers.ValidationError("Topping does not exist")

                size = item.pop("size")
                try:
                    size = Size.objects.get(pk=size.get("id"))
                except Size.DoesNotExist:
                    # data = {"error": "Bad Request (400)"}
                    raise serializers.ValidationError("Size does not exist")

                order_item.topping = topping
                order_item.size = size
                new_items.append(order_item)
                # OrderItem.objects.create(order=instance, topping=topping, size=size, **item)

        instance.is_made = validated_data.get("is_made", instance.is_made)
        instance.is_dispatched = validated_data.get(
            "is_dispatched", instance.is_dispatched
        )
        instance.is_collected = validated_data.get(
            "is_collected", instance.is_collected
        )
        instance.is_delivered = validated_data.get(
            "is_delivered", instance.is_delivered
        )
        instance.customer = customer
        instance.save()
        return instance