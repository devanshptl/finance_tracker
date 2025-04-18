from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Wallet, Income
from .serializers import ExpenseSerializer, WalletSerializer, IncomeSerializer
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404


class ExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Expense, pk=pk, user=user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            expenses = Expense.objects.filter(user=request.user).order_by("-date")
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        else:
            expense = self.get_object(pk, request.user)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  # Wallet balance is updated in serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        expense = self.get_object(pk, request.user)
        serializer = ExpenseSerializer(
            expense, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()  # Wallet balance is updated in serializer
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        expense = self.get_object(pk, request.user)
        serializer = ExpenseSerializer(
            expense, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()  # Wallet balance is updated in serializer
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        expense = self.get_object(pk, request.user)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        wallet, created = Wallet.objects.get_or_create(user=request.user)

        amount = request.data.get("balance")
        if amount is None:
            return Response(
                {"error": "Balance amount is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = Decimal(amount)  # Convert to Decimal
        except (ValueError, InvalidOperation):
            return Response(
                {"error": "Invalid balance amount."}, status=status.HTTP_400_BAD_REQUEST
            )

        wallet.balance += amount
        wallet.save()

        serializer = WalletSerializer(wallet)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class IncomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Income, pk=pk, user=user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            incomes = Income.objects.filter(user=request.user).order_by("-date")
            serializer = IncomeSerializer(incomes, many=True)
            return Response(serializer.data)
        else:
            income = self.get_object(pk, request.user)
            serializer = IncomeSerializer(income)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IncomeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  # Wallet balance is updated in serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        income = self.get_object(pk, request.user)
        serializer = IncomeSerializer(
            income, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        income = self.get_object(pk, request.user)
        serializer = IncomeSerializer(
            income, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        income = self.get_object(pk, request.user)
        income.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
