from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Wallet
from .serializers import ExpenseSerializer, WalletSerializer
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from decimal import Decimal, InvalidOperation


class ExpenseListCreateAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save()


class ExpenseUpdateAPIView(UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        expense = super().get_object()
        if expense.user != self.request.user:
            raise PermissionDenied("You can only update your own expenses.")
        return expense

    def perform_update(self, serializer):
        expense = self.get_object()
        old_amount = expense.amount
        new_amount = serializer.validated_data.get("amount", old_amount)

        if new_amount != old_amount:
            profile = Wallet.objects.get(user=self.request.user)
            profile.balance += old_amount - new_amount
            profile.save()

        serializer.save()


# For PATCH requests, perform partial updates
class ExpensePartialUpdateAPIView(ExpenseUpdateAPIView):
    http_method_names = ["patch"]


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
