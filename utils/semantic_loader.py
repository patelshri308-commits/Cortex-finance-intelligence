import yaml


def load_semantic_model(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def build_metric_context(semantic_model):
    metrics = semantic_model.get("metrics", {})

    context_lines = []

    for metric_name, metric_info in metrics.items():
        definition = metric_info.get("definition", "")
        interpretation = metric_info.get("interpretation", "")

        context_lines.append(
            f"""
Metric: {metric_name}
Definition: {definition}
Business Interpretation: {interpretation}
"""
        )

    return "\n".join(context_lines)
