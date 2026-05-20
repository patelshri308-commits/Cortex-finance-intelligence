from pathlib import Path

import pandas as pd


def export_finance_report() -> str:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "cortex_finance_report.xlsx"

    monthly_kpis = pd.read_csv("data/monthly_kpis.csv")

    output_files = {
        "Revenue Summary Agent": "outputs/revenue_summary.txt",
        "Variance Analysis Agent": "outputs/variance_analysis.txt",
        "Forecast Sensitivity Agent": "outputs/forecast_sensitivity.txt",
        "Executive Briefing Agent": "outputs/executive_briefing.txt",
    }

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        monthly_kpis.to_excel(
            writer,
            sheet_name="Monthly KPIs",
            index=False
        )

        executive_summary = []

        for agent_name, file_path in output_files.items():
            path = Path(file_path)

            if path.exists():
                text = path.read_text()
            else:
                text = "Output has not been generated yet."

            executive_summary.append({
                "Workflow": agent_name,
                "Output": text
            })

            agent_df = pd.DataFrame(
                [{"Generated Output": text}]
            )

            agent_df.to_excel(
                writer,
                sheet_name=agent_name[:31],
                index=False
            )

        summary_df = pd.DataFrame(executive_summary)

        summary_df.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

    return str(report_path)


def main():
    report_path = export_finance_report()

    print(f"Finance report exported to {report_path}")


if __name__ == "__main__":
    main()
