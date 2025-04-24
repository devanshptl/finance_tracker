from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
import base64
import datetime

from .analytics import get_monthly_summary
from .charts import (
    plot_monthly_income_expense,
    plot_expense_category_pie,
)


def generate_monthly_report_pdf(user):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Finance Report - {user.username}")
    c.setFont("Helvetica", 12)
    c.drawString(
        50,
        height - 70,
        f"Generated on: {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}",
    )

    # Monthly Summary Table
    summary_df = get_monthly_summary(user)
    summary_data = [
        [
            "Month",
            "Income",
            "Expense",
            "Net Savings",
            "Saving Rate (%)",
            "Top Expense Category",
        ]
    ]
    for _, row in summary_df.iterrows():
        summary_data.append(
            [
                row["month"],
                f"₹{row['income']:.2f}",
                f"₹{row['expense']:.2f}",
                f"₹{row['net_savings']:.2f}",
                f"{row['saving_rate']}%",
                row.get("top_expense_category", "N/A"),
            ]
        )

    table = Table(summary_data, colWidths=[70, 70, 70, 80, 90, 130])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )

    table.wrapOn(c, width, height)
    table.drawOn(c, 30, height - 350)

    # Charts Section
    for title, base64_img in [
        ("Monthly Income vs Expense", plot_monthly_income_expense(user)),
        ("Category-wise Expense Distribution", plot_expense_category_pie(user)),
    ]:
        if base64_img:
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 50, title)

            img_data = io.BytesIO(base64.b64decode(base64_img))
            c.drawImage(
                ImageReader(img_data),
                50,
                100,
                width=500,
                preserveAspectRatio=True,
                mask="auto",
            )

    c.save()
    buffer.seek(0)
    return buffer
