from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Investment
from .serializers import InvestmentSerializer
from rest_framework.exceptions import ValidationError


class BuyInvestmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Filter buy transactions where quantity > 0
        investments = Investment.objects.filter(
            user=request.user, transaction_type="buy", quantity__gt=0
        )
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Handle creating a new buy investment
        serializer = InvestmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Handle updating an existing buy investment
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        serializer = InvestmentSerializer(
            investment, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Handle partial update for a buy investment
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        serializer = InvestmentSerializer(
            investment, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellInvestmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all sell transactions for the user
        investments = Investment.objects.filter(
            user=request.user, transaction_type="sell"
        )
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Handle creating a new sell investment
        serializer = InvestmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Handle updating an existing sell investment
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        serializer = InvestmentSerializer(
            investment, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Handle partial update for a sell investment
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        serializer = InvestmentSerializer(
            investment, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    InvestmentSerializer(instance).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
