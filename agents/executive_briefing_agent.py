import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import os
from pathlib import Path

import google.generativeai as genai
import yaml
from dotenv import load_dotenv

from agents.revenue_summary_agent import generate_revenue_summary
from agents.variance_analysis_agent import generate_variance_analysis

from utils.schema_validation import validate_monthly_kpis


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def generate_executive_briefing() -> str:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3.5-flash")

    prompt_config = load_prompt_config("prompts/executive_briefing.yaml")

    revenue_summary = generate_revenue_summary()
    variance_analysis = generate_variance_analysis()

    context = f"""
Revenue Summary Agent Output:
{revenue_summary}

Variance Analysis Agent Output:
{variance_analysis}
"""

    prompt = f"""
{prompt_config["system_prompt"]}

{prompt_config["output_format"]}

Use the following agent outputs as source material.

{context}
"""

    response = model.generate_content(prompt)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "executive_briefing.txt"

    with open(output_path, "w") as file:
        file.write(response.text)

    return response.text


def main():
    briefing = generate_executive_briefing()

    print("\nAI Executive Briefing")
    print("---------------------")
    print(briefing)
    print("\nSaved output to outputs/executive_briefing.txt")


if __name__ == "__main__":
    main()
