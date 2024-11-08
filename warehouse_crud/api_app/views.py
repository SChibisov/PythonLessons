from django.db.models import F
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User, Cart
from .serializers import ProductsSerializer, UsersSerializer, CartSerializer


class UserControllerList(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UsersSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserControllerDetail(APIView):
    # Get - get user by PK
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UsersSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404

    # PUT - add new user
    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductControllerList(APIView):
    def get(self, request, format=None):
        items = Product.objects.all()
        serializer = ProductsSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductControllerDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductsSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartControllerDetail(APIView):
    """
    Корзина пользователя
    """
    """
    Метод получения корзины пользователя 
    """

    def get(self, request, pk, format=None):
        cart = Cart.objects.filter(user_mail=pk)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    """
    Добавить в корзину для пользователя
    """

    def post(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        product_id = request.data['product_id']
        product = Product.objects.get(pk=product_id)
        product_count = request.data['product_count']
        product_is_available = Product.is_available
        if not product_is_available:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # cart_item, created = Cart.objects.get_or_create(
        #     user_mail=user,
        #     product_id=product,
        #     product_count_id=product_count
        # )
        cart = Cart.objects.get(user)
        if not cart:
            cart.product_count += product_count
            product_count_update = Product.objects.update(product_count=F("product_count") - 1)
            product_count_update.save()
            cart.save()
        else:
            cart.product_count = product_count
            cart.save()

        # cart = Cart(user_mail=user, product_id=product, product_count_id=product_count)
        # cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    """
    Очистить корзину пользователя
    """

    def delete(self, request, pk, format=None):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
