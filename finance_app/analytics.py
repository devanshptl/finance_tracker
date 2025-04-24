import pandas as pd
from .models import Expense, Income


def get_monthly_summary(user):
    income_qs = Income.objects.filter(user=user).values("amount", "date", "category")
    expense_qs = Expense.objects.filter(user=user).values("amount", "date", "category")

    income_df = pd.DataFrame(income_qs)
    expense_df = pd.DataFrame(expense_qs)

    for df in [income_df, expense_df]:
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M").astype(str)

    income_summary = income_df.groupby("month")["amount"].sum()
    expense_summary = expense_df.groupby("month")["amount"].sum()

    summary_df = pd.concat([income_summary, expense_summary], axis=1).fillna(0)
    summary_df.columns = ["income", "expense"]
    summary_df["net_savings"] = summary_df["income"] - summary_df["expense"]
    summary_df["saving_rate"] = summary_df.apply(
        lambda row: (
            round((row["net_savings"] / row["income"]) * 100, 2)
            if row["income"] > 0
            else 0.0
        ),
        axis=1,
    )

    if not expense_df.empty:
        top_categories = (
            expense_df.groupby(["month", "category"])["amount"]
            .sum()
            .reset_index()
            .sort_values(["month", "amount"], ascending=[True, False])
        )
        top_expense = (
            top_categories.groupby("month")
            .first()["category"]
            .rename("top_expense_category")
        )
        summary_df = summary_df.join(top_expense)

    return summary_df.reset_index()
