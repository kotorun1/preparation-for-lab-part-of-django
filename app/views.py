from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_401_UNAUTHORIZED, HTTP_200_OK, \
    HTTP_404_NOT_FOUND

from .models import CustomUser, Product, Cart, Order
from .serializer import CustomUserSerializer, AuthTokenSerializer
from .serializer import ProductSerializer, CartSerializer, OrderSerializer


@api_view(["POST"])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({
                "data": {
                    "user_token": token.key
                }
            }, status=HTTP_201_CREATED)
        return Response({"error":
            {
                "code": 422,
                "message": "Нарушение правил валидации",
                "errors": serializer.errors
            }}, status=HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
def auth(request):
    if request.method == 'POST':
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'body': {
                'user_token': token.key
            }}, status=HTTP_200_OK)
        return Response({"error":
            {
                "code": 401,
                "message": "Authentication failed",
            }}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'GET':
        request.user.auth_token.delete()
        return Response({'body':
            {
                "message":
                    "logout"
            }}, status=HTTP_200_OK)


# прошёл час


@api_view(['GET'])
def listProductsView(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'body': serializer.data
        }, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProductView(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'body':
                {
                    "id": serializer.data['id'],
                    "message": "Product added"
                }},HTTP_201_CREATED)
        return Response({"error":
            {
                "code": 422,
                "message": "Нарушение правил валидации",
                "errors": serializer.errors
            }}, status=HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def detailProductView(request, id):
    try:
        item = Product.objects.get(pk=id)
    except:
        return Response({
            "error": {
                "code": 404,
                "message": "Не найдено"
            }
        }, status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(item)
        return Response({
            'body': serializer.data
        }, status=HTTP_200_OK)
    if request.method == 'PATCH':
        serializer = ProductSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'body': serializer.data
            }, status=HTTP_200_OK)
        return Response({"error":
            {
                "code": 422,
                "message": "Нарушение правил валидации",
                "errors": serializer.errors
            }}, status=HTTP_422_UNPROCESSABLE_ENTITY)
    if request.method == 'DELETE':
        item.delete()
        return Response({"body": {'message': "Product removed"}}, status=HTTP_200_OK)


# до сюда дошел


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def createCartView(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except:
        return Response({
            "error": {
                "code": 404,
                "message": "Не найдено"
            }
        }, status=HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return Response({'body': {
            "message": "Product add to cart"
        }}, HTTP_201_CREATED)

    if request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        return Response({"body": {'message': "Item removed from cart"}}, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCartView(request):
    try:
        item = Cart.objects.get(user=request.user)
    except:
        return Response({
            "error": {
                "code": 404,
                "message": "Не найдено"
            }
        }, status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CartSerializer(item)
        return Response({
            'body': serializer.data
        }, status=HTTP_200_OK)


# 47 минут делал корзину

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orderView(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response({'body':
                             serializer.data
                         })
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return Response({'error': {
                "code": 422,
                "message": "Cart is empty",
            }})
        order = Order.objects.create(user=request.user)
        results = Cart.objects.all()
        for staff in results:
            for product in staff.products.all():
                order.products.add(product)
        order.save()
        cart.delete()
        serializer = OrderSerializer(order)
        return Response({"body": {
            "order_id": 1,
            "message": "Order is processed",
        }},status=HTTP_201_CREATED)
# через 47 минут
# 13 минут проверял