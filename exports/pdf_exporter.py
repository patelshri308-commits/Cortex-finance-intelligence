from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path("outputs/executive_briefing.pdf")
KPI_PATH = Path("data/monthly_kpis.csv")
EXECUTIVE_BRIEFING_PATH = Path("outputs/executive_briefing.txt")


def _format_currency(value: float) -> str:
    return f"${float(value):,.0f}"


def _format_signed_currency(value: float) -> str:
    amount = float(value)
    sign = "+" if amount >= 0 else "-"
    return f"{sign}${abs(amount):,.0f}"


def _format_month(value: object) -> str:
    month = pd.to_datetime(value, errors="coerce")
    if pd.isna(month):
        return "Unknown"
    return month.strftime("%b %Y")


def _read_executive_briefing() -> str:
    if not EXECUTIVE_BRIEFING_PATH.exists():
        return "Executive briefing output has not been generated yet."
    return EXECUTIVE_BRIEFING_PATH.read_text(encoding="utf-8").strip()


def _extract_section(text: str, headings: list[str]) -> str:
    lines = text.splitlines()
    capture = False
    captured_lines: list[str] = []
    normalized_headings = {heading.lower() for heading in headings}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped.removeprefix("## ").strip().lower()
            if capture:
                break
            capture = heading in normalized_headings
            continue

        if capture:
            captured_lines.append(line)

    return "\n".join(captured_lines).strip()


def _strip_markdown_headings(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            continue
        lines.append(raw_line)
    return "\n".join(lines).strip()


def _markdown_to_paragraphs(text: str, styles) -> list:
    flowables: list = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flowables.append(Spacer(1, 0.08 * inch))
            continue

        if line.startswith("## "):
            flowables.append(Paragraph(line.removeprefix("## ").strip(), styles["SectionHeading"]))
        elif line.startswith("- "):
            flowables.append(Paragraph(f"&bull; {line.removeprefix('- ').strip()}", styles["Body"]))
        else:
            flowables.append(Paragraph(line, styles["Body"]))

    return flowables


def _build_metric_table(rows: list[list[str]], column_widths: list[float] | None = None) -> Table:
    widths = column_widths or [2.4 * inch, 3.6 * inch]
    table = Table(rows, colWidths=widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _build_finance_snapshot() -> dict[str, object]:
    if not KPI_PATH.exists():
        fallback_rows = [["Metric", "Value"], ["KPI data", "data/monthly_kpis.csv not found"]]
        return {
            "latest_month": "Unknown",
            "arr_bridge_rows": fallback_rows,
            "growth_driver_rows": [["Driver", "Value"], ["KPI data", "Unavailable"]],
            "headwind_rows": [["Headwind", "Value"], ["KPI data", "Unavailable"]],
        }

    df = pd.read_csv(KPI_PATH)
    if df.empty or len(df) < 2:
        fallback_rows = [["Metric", "Value"], ["KPI data", "Not enough monthly KPI rows"]]
        return {
            "latest_month": "Unknown",
            "arr_bridge_rows": fallback_rows,
            "growth_driver_rows": [["Driver", "Value"], ["KPI data", "Insufficient history"]],
            "headwind_rows": [["Headwind", "Value"], ["KPI data", "Insufficient history"]],
        }

    df.columns = [col.lower() for col in df.columns]
    df["revenue_month"] = pd.to_datetime(df["revenue_month"], errors="coerce")
    df = df.sort_values("revenue_month")

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    starting_arr = float(previous["total_arr"])
    ending_arr = float(latest["total_arr"])
    new_arr_bookings = float(latest.get("new_business_revenue", latest["total_bookings"]))
    expansion_revenue = float(latest["expansion_revenue"])
    churned_revenue = float(latest["churned_revenue"])
    contraction_revenue = float(latest["contraction_revenue"])
    arr_movement = ending_arr - starting_arr
    growth_drivers = new_arr_bookings + expansion_revenue
    retention_headwinds = churned_revenue + contraction_revenue
    latest_month = _format_month(latest["revenue_month"])

    arr_bridge_rows = [
        ["Metric", "Value"],
        ["Latest Month", latest_month],
        ["Starting ARR", _format_currency(starting_arr)],
        ["New ARR Bookings", _format_currency(new_arr_bookings)],
        ["Expansion ARR", _format_currency(expansion_revenue)],
        ["Churned ARR", f"-{_format_currency(churned_revenue)}"],
        ["Contraction ARR", f"-{_format_currency(contraction_revenue)}"],
        ["Ending ARR", _format_currency(ending_arr)],
        ["Net ARR Movement", _format_signed_currency(arr_movement)],
    ]

    growth_driver_rows = [
        ["Growth Driver", "Value"],
        ["New ARR Bookings", _format_currency(new_arr_bookings)],
        ["Expansion ARR", _format_currency(expansion_revenue)],
        ["Total Growth Drivers", _format_currency(growth_drivers)],
    ]

    headwind_rows = [
        ["Headwind", "Value"],
        ["Churned ARR", _format_currency(churned_revenue)],
        ["Contraction ARR", _format_currency(contraction_revenue)],
        ["Total Retention Headwinds", _format_currency(retention_headwinds)],
    ]

    return {
        "latest_month": latest_month,
        "arr_bridge_rows": arr_bridge_rows,
        "growth_driver_rows": growth_driver_rows,
        "headwind_rows": headwind_rows,
    }


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleMain",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#111827"),
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151"),
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Intro",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#374151"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Muted",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#6B7280"),
            spaceAfter=6,
        )
    )
    return styles


def generate_executive_pdf() -> str:
    """Generate a local executive finance briefing PDF and return its path."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    styles = _build_styles()
    briefing_text = _read_executive_briefing()
    executive_summary = _strip_markdown_headings(briefing_text)
    key_risks = _extract_section(briefing_text, ["Key Risk", "Key Risks"])
    leadership_actions = _extract_section(briefing_text, ["Leadership Takeaway", "Leadership Actions"])
    finance_snapshot = _build_finance_snapshot()
    generated_timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")

    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="Executive Finance Briefing",
    )

    elements: list = [
        Paragraph("Executive Finance Briefing", styles["TitleMain"]),
        Paragraph(f"Generated: {generated_timestamp}", styles["Muted"]),
        Paragraph(f"Latest KPI Month: {finance_snapshot['latest_month']}", styles["Muted"]),
        Spacer(1, 0.12 * inch),
        Paragraph("Executive Summary", styles["SectionHeading"]),
        Paragraph(
            "This briefing packages the latest saved finance-agent narrative with local KPI data for leadership review.",
            styles["Intro"],
        ),
        *_markdown_to_paragraphs(executive_summary, styles),
        Paragraph("ARR Bridge", styles["SectionHeading"]),
        Paragraph(
            "The bridge below summarizes the latest month movement from starting ARR to ending ARR.",
            styles["Intro"],
        ),
        _build_metric_table(finance_snapshot["arr_bridge_rows"]),
        Spacer(1, 0.1 * inch),
        Paragraph("Growth Drivers", styles["SectionHeading"]),
        Paragraph(
            "Growth drivers represent new and expansion recurring revenue contributing positive ARR movement.",
            styles["Intro"],
        ),
        _build_metric_table(finance_snapshot["growth_driver_rows"]),
        Spacer(1, 0.1 * inch),
        Paragraph("Headwinds", styles["SectionHeading"]),
        Paragraph(
            "Headwinds represent retention pressure from churned and contracted recurring revenue.",
            styles["Intro"],
        ),
        _build_metric_table(finance_snapshot["headwind_rows"]),
        Spacer(1, 0.1 * inch),
    ]

    elements.append(Paragraph("Key Risks", styles["SectionHeading"]))
    elements.extend(_markdown_to_paragraphs(key_risks or "No key risk section found in saved executive briefing.", styles))

    elements.append(Paragraph("Leadership Actions", styles["SectionHeading"]))
    elements.extend(
        _markdown_to_paragraphs(
            leadership_actions or "No leadership actions section found in saved executive briefing.",
            styles,
        )
    )

    document.build(elements)
    return str(OUTPUT_PATH)


def main():
    report_path = generate_executive_pdf()
    print(f"Executive briefing PDF exported to {report_path}")


if __name__ == "__main__":
    main()
