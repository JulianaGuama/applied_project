from __future__ import annotations


class ProblemEvaluator:
    def __init__(self, definition: dict):
        self.definition = definition

    def evaluate(self, row: dict) -> dict:
        metrics = self.definition["metrics"]
        breaches: list[str] = []

        if float(row["csat"]) < float(metrics["csat"]["threshold_min"]):
            breaches.append("csat abaixo do mínimo")
        if float(row["first_response_minutes"]) > float(metrics["first_response_minutes"]["threshold_max"]):
            breaches.append("tempo de primeira resposta acima do máximo")
        if float(row["resolution_rate"]) < float(metrics["resolution_rate"]["threshold_min"]):
            breaches.append("taxa de resolução abaixo do mínimo")
        if float(row["escalation_rate"]) > float(metrics["escalation_rate"]["threshold_max"]):
            breaches.append("taxa de escalonamento acima do máximo")

        has_problem = len(breaches) > 0

        return {
            "has_problem": has_problem,
            "breaches": breaches,
            "message": (
                "problema identificado" if has_problem else self.definition["logic"]["no_action_message"]
            ),
        }
