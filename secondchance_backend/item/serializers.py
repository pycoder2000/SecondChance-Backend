from rest_framework import serializers
from .models import Item, Rental
from useraccount.serializers import UserDetailSerializer


class ItemsListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing items with basic details.
    """

    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = (
            "id",
            "title",
            "rental_price",
            "image_url",
            "category",
            "condition",
            "location",
        )


class ItemsDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed item view with additional information.
    """

    seller = UserDetailSerializer(read_only=True, many=False)
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = (
            "id",
            "title",
            "description",
            "rental_price",
            "image_url",
            "seller",
            "category",
            "condition",
            "location",
            "quantity",
        )


class RentalsListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing rentals with item details.
    """

    item = ItemsListSerializer(read_only=True, many=False)

    class Meta:
        model = Rental
        fields = (
            "id",
            "start_date",
            "end_date",
            "number_of_days",
            "total_price",
            "item",
            "quantity",
        )
