from django.forms import ModelForm
from .models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = (
            "title",
            "description",
            "rental_price",
            "quantity",
            "condition",
            "category",
            "country",
            "country_code",
            "image",
        )
