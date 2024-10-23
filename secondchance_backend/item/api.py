from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.tokens import AccessToken
from .forms import ItemForm
from .models import Item, Rental
from .serializers import (
    ItemsListSerializer,
    ItemsDetailSerializer,
    RentalsListSerializer,
)
from useraccount.models import User


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def items_list(request):
    # Authentication
    try:
        token = request.META["HTTP_AUTHORIZATION"].split("Bearer ")[1]
        token = AccessToken(token)
        user_id = token.payload["user_id"]
        user = User.objects.get(pk=user_id)
    except Exception:
        user = None

    # Favorites handling
    favorites = []
    properties = Item.objects.all()

    # Filtering
    is_favorites = request.GET.get("is_favorites", "")
    seller_id = request.GET.get("seller_id", "")
    country = request.GET.get("country", "")
    category = request.GET.get("category", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date and end_date:
        exact_matches = Rental.objects.filter(
            start_date=start_date
        ) | Rental.objects.filter(end_date=end_date)
        overlap_matches = Rental.objects.filter(
            start_date__lte=end_date, end_date__gte=start_date
        )
        all_matches = set(exact_matches.values_list("item_id", flat=True)) | set(
            overlap_matches.values_list("item_id", flat=True)
        )
        properties = properties.exclude(id__in=all_matches)

    if seller_id:
        properties = properties.filter(seller_id=seller_id)

    if is_favorites and user:
        properties = properties.filter(favorited__in=[user])

    if country:
        properties = properties.filter(country=country)

    if category and category != "undefined":
        properties = properties.filter(category=category)

    # Marking favorites
    if user:
        favorites = properties.filter(favorited__in=[user]).values_list("id", flat=True)

    serializer = ItemsListSerializer(properties, many=True)

    return JsonResponse({"data": serializer.data, "favorites": list(favorites)})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        serializer = ItemsDetailSerializer(item, many=False)
        return JsonResponse(serializer.data)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def item_rentals(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        rentals = item.rentals.all()
        serializer = RentalsListSerializer(rentals, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)


@api_view(["POST"])
def create_item(request):
    form = ItemForm(request.POST, request.FILES)
    if form.is_valid():
        item = form.save(commit=False)
        item.seller = request.user
        item.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"errors": form.errors.as_json()}, status=400)


@api_view(["POST"])
def buy_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        Rental.objects.create(
            item=item,
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            number_of_days=request.POST.get("number_of_days"),
            total_price=request.POST.get("total_price"),
            quantity=request.POST.get("quantity"),
            created_by=request.user,
        )
        return JsonResponse({"success": True})
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["POST"])
def toggle_favorite(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        if request.user in item.favorited.all():
            item.favorited.remove(request.user)
            return JsonResponse({"is_favorite": False})
        else:
            item.favorited.add(request.user)
            return JsonResponse({"is_favorite": True})
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
