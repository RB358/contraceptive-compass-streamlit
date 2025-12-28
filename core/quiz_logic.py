from typing import List, Dict, Any

def evaluate_method(method: Dict[str, Any], encoded: Dict[str, Any]) -> str:
    name = method["name"]
    
    has_smoke_heavy = encoded["has_smoke_heavy"]
    has_clot = encoded["has_clot"]
    has_migraine = encoded["has_migraine"]
    has_bp = encoded["has_bp"]
    is_breastfeeding = encoded["is_breastfeeding"]
    priority = encoded["priority"]
    
    red = False
    
    if "Pill" in name or "Patch" in name or "Ring" in name:
        if has_smoke_heavy or has_clot or has_migraine or has_bp:
            red = True
    
    if "Implant" in name or "Hormonal IUD" in name or "Depo" in name:
        if has_clot:
            red = True
    
    if is_breastfeeding and ("hormonal" in name.lower() or "Pill" in name or "Patch" in name or "Ring" in name or "Implant" in name or "Hormonal IUD" in name or "Depo" in name):
        if red:
            return "contraindicated"
        return "caution"
    
    if red:
        return "contraindicated"
    
    if priority == "Highest effectiveness" and method["typical"] == "<1%":
        return "recommended"
    elif priority == "Avoiding hormones" and ("Copper IUD" in name or "Condom" in name or "Diaphragm" in name or "Fertility Awareness" in name):
        return "recommended"
    elif priority == "Managing periods" and "Lighter periods" in method["pros"]:
        return "recommended"
    elif priority == "Low maintenance (set and forget)" and ("years" in " ".join(method["pros"]) or "3 months" in " ".join(method["pros"])):
        return "recommended"
    elif priority == "Quick return to fertility" and ("Condom" in name or "Diaphragm" in name or "Fertility Awareness" in name):
        return "recommended"
    
    return "caution"


def get_recommendations(methods: List[Dict[str, Any]], encoded: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    results = {
        "recommended": [],
        "caution": [],
        "contraindicated": []
    }
    
    for method in methods:
        category = evaluate_method(method, encoded)
        results[category].append(method)
    
    return results
