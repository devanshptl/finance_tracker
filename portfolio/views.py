from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Investment
from .serializers import InvestmentSerializer
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
import pandas as pd


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


class StartSIPAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all active SIP investments for the user
        investments = Investment.objects.filter(
            user=request.user, asset_type="sip", is_sip_active=True
        )
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Handle creating a new SIP investment (starting an SIP)
        serializer = InvestmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                investment = serializer.save()
                # Start SIP logic
                investment.is_sip_active = True
                investment.sip_start_date = timezone.now().date()
                investment.next_sip_date = investment.sip_start_date
                investment.save()
                # Initialize SIP task (optional)
                investment.initialize_sip()

                return Response(
                    InvestmentSerializer(investment).data,
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Handle updating an existing SIP investment (starting SIP if not started)
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        if investment.asset_type != "sip":
            return Response(
                {"detail": "This is not an SIP investment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if investment.is_sip_active:
            return Response(
                {"detail": "This SIP is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvestmentSerializer(
            investment, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                # Start SIP logic
                investment.is_sip_active = True
                investment.sip_start_date = timezone.now().date()
                investment.next_sip_date = investment.sip_start_date
                investment.save()

                # Initialize SIP task (optional)
                investment.initialize_sip()

                return Response(
                    InvestmentSerializer(investment).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Handle partial update for an SIP investment (start SIP if not started)
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        if investment.asset_type != "sip":
            return Response(
                {"detail": "This is not an SIP investment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if investment.is_sip_active:
            return Response(
                {"detail": "This SIP is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvestmentSerializer(
            investment, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            try:
                # Start SIP logic
                investment.is_sip_active = True
                investment.sip_start_date = timezone.now().date()
                investment.next_sip_date = investment.sip_start_date
                investment.save()

                # Initialize SIP task (optional)
                investment.initialize_sip()

                return Response(
                    InvestmentSerializer(investment).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StopSIPAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all active SIP investments for the user
        investments = Investment.objects.filter(
            user=request.user, asset_type="sip", is_sip_active=True
        )
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Handle creating a new stop SIP transaction
        serializer = InvestmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                investment = serializer.save()
                # Stop SIP logic
                investment.is_sip_active = False
                investment.save()

                return Response(
                    InvestmentSerializer(investment).data,
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Handle updating an existing SIP investment (stopping SIP)
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        if investment.asset_type != "sip":
            return Response(
                {"detail": "This is not an SIP investment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not investment.is_sip_active:
            return Response(
                {"detail": "This SIP is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvestmentSerializer(
            investment, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                # Stop SIP logic
                investment.is_sip_active = False
                investment.save()

                return Response(
                    InvestmentSerializer(investment).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Handle partial update for stopping SIP
        investment = get_object_or_404(Investment, pk=pk, user=request.user)
        if investment.asset_type != "sip":
            return Response(
                {"detail": "This is not an SIP investment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not investment.is_sip_active:
            return Response(
                {"detail": "This SIP is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvestmentSerializer(
            investment, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            try:
                # Stop SIP logic
                investment.is_sip_active = False
                investment.save()

                return Response(
                    InvestmentSerializer(investment).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Only consider "buy" transactions for portfolio analysis
        investments = Investment.objects.filter(user=user, transaction_type="buy")

        if not investments.exists():
            return Response({"message": "No investments found."}, status=404)

        # Build data from investments
        data = []
        for inv in investments:
            data.append(
                {
                    "name": inv.name,
                    "symbol": inv.symbol,
                    "asset_type": inv.asset_type,
                    "quantity": inv.quantity,
                    "buy_price": inv.price,  # buy price is "price" field
                    "current_price": inv.current_price or inv.price,  # fallback
                    "date_invested": inv.date,
                    "invested_value": inv.total_invested(),
                    "current_value": inv.current_value(),
                    "return_percentage": inv.returns_percentage(),
                }
            )

        df = pd.DataFrame(data)

        # 1. Time-series Portfolio Growth
        portfolio_growth = (
            df.groupby("date_invested")[["invested_value", "current_value"]]
            .sum()
            .cumsum()
        )

        time_series = {
            "dates": pd.to_datetime(portfolio_growth.index)
            .strftime("%Y-%m-%d")
            .tolist(),
            "invested_value": portfolio_growth["invested_value"].tolist(),
            "current_value": portfolio_growth["current_value"].tolist(),
        }

        # 2. Investment by Asset Type
        asset_distribution = df.groupby("asset_type")["current_value"].sum()

        asset_breakdown = {
            "labels": asset_distribution.index.tolist(),
            "values": asset_distribution.values.tolist(),
        }

        # 3. Top Performers
        top_performers = df.sort_values(by="return_percentage", ascending=False).head(5)
        top_performers_list = top_performers[
            ["name", "symbol", "return_percentage"]
        ].to_dict(orient="records")

        # 4. Volatility
        volatility = df["return_percentage"].std()

        # Final Response
        return Response(
            {
                "time_series": time_series,
                "asset_breakdown": asset_breakdown,
                "top_performers": top_performers_list,
                "volatility": round(volatility, 2),
                "total_invested": round(df["invested_value"].sum(), 2),
                "current_portfolio_value": round(df["current_value"].sum(), 2),
                "overall_returns_percentage": (
                    round(
                        (
                            (df["current_value"].sum() - df["invested_value"].sum())
                            / df["invested_value"].sum()
                        )
                        * 100,
                        2,
                    )
                    if df["invested_value"].sum()
                    else 0
                ),
            }
        )
