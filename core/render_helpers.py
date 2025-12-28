from typing import List, Dict, Any

def format_method_card_html(method: Dict[str, Any]) -> str:
    return (
        f"<div class='method-card'><h3>{method['name']}</h3>"
        f"<p><strong>Perfect use:</strong> {method['perfect']} failure<br>"
        f"<strong>Typical use:</strong> {method['typical']} failure</p>"
        f"<p><strong>Pros:</strong> {', '.join(method['pros'])}</p>"
        f"<p><strong>Cons:</strong> {', '.join(method['cons'])}</p></div>"
    )


def format_recommendation_text(method: Dict[str, Any], include_failure: bool = True) -> str:
    if include_failure:
        return f"- {method['name']} ({method['typical']} typical failure)"
    return f"- {method['name']}"


def format_telehealth_link(service: Dict[str, str]) -> str:
    return f"[{service['name']} →]({service['url']})"
