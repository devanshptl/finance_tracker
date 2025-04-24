import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import seaborn as sns
from matplotlib.patches import Circle
from .models import Income, Expense

sns.set(style="whitegrid")


def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def plot_monthly_income_expense(user):
    from .analytics import get_monthly_summary

    df = get_monthly_summary(user)
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = range(len(df))
    ax.bar(
        [i - width / 2 for i in x], df["income"], width, label="Income", color="green"
    )
    ax.bar(
        [i + width / 2 for i in x], df["expense"], width, label="Expense", color="red"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(df["month"], rotation=45)
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Monthly Income vs Expense")
    ax.legend()
    fig.tight_layout()
    return _fig_to_base64(fig)


def plot_expense_category_pie(user):
    expense_qs = Expense.objects.filter(user=user).values("amount", "category")
    expense_df = pd.DataFrame(expense_qs)

    if expense_df.empty:
        return None

    category_sum = expense_df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        category_sum,
        labels=category_sum.index,
        autopct="%1.1f%%",
        startangle=140,
        textprops=dict(color="black", fontsize=10),
        wedgeprops=dict(width=0.5),
    )

    ax.set_title("Expense Distribution by Category", fontsize=14, fontweight="bold")
    plt.setp(autotexts, size=10, weight="bold")

    centre_circle = Circle((0, 0), 0.30, fc="white")
    ax.add_artist(centre_circle)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()

    return _fig_to_base64(fig)
