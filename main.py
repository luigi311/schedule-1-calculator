#!/usr/bin/env python3
import argparse
import itertools
from typing import List, Set, Tuple, Dict

# Thank you https://schedule1-calculator.com/howitworks
INTERACTIONS: Dict[str, Dict[str, str]] = {
    "Cuke": {
        "Euphoric": "Laxative",
        "Foggy": "Cyclopean",
        "Gingeritis": "Thought-Provoking",
        "Munchies": "Athletic",
        "Slippery": "Munchies",
        "Sneaky": "Paranoia",
        "Toxic": "Euphoric",
    },
    "Flu Medicine": {
        "Athletic": "Munchies",
        "Calming": "Bright-Eyed",
        "Cyclopean": "Foggy",
        "Electrifying": "Refreshing",
        "Euphoric": "Toxic",
        "Focused": "Calming",
        "Laxative": "Euphoric",
        "Munchies": "Slippery",
        "Shrinking": "Paranoia",
        "Thought-Provoking": "Gingeritis",
    },
    "Gasoline": {
        "Disorienting": "Glowing",
        "Electrifying": "Disorienting",
        "Energizing": "Euphoric",
        "Euphoric": "Spicy",
        "Gingeritis": "Smelly",
        "Jennerising": "Sneaky",
        "Laxative": "Foggy",
        "Munchies": "Sedating",
        "Paranoia": "Calming",
        "Shrinking": "Focused",
        "Sneaky": "Tropic Thunder",
    },
    "Donut": {
        "Anti-Gravity": "Slippery",
        "Balding": "Sneaky",
        "Calorie-Dense": "Explosive",
        "Focused": "Euphoric",
        "Jennerising": "Gingeritis",
        "Munchies": "Calming",
        "Shrinking": "Energizing",
    },
    "Energy Drink": {
        "Disorienting": "Electrifying",
        "Euphoric": "Energizing",
        "Focused": "Shrinking",
        "Foggy": "Laxative",
        "Glowing": "Disorienting",
        "Schizophrenia": "Balding",
        "Sedating": "Munchies",
        "Spicy": "Euphoric",
        "Tropic Thunder": "Sneaky",
    },
    "Mouth Wash": {
        "Calming": "Anti-Gravity",
        "Calorie-Dense": "Sneaky",
        "Explosive": "Sedating",
        "Focused": "Jennerising",
    },
    "Motor Oil": {
        "Energizing": "Munchies",
        "Euphoric": "Sedating",
        "Foggy": "Toxic",
        "Munchies": "Schizophrenia",
        "Paranoia": "Anti-Gravity",
    },
    "Banana": {
        "Calming": "Sneaky",
        "Cyclopean": "Energizing",
        "Disorienting": "Focused",
        "Energizing": "Thought-Provoking",
        "Focused": "Seizure-Inducing",
        "Long Faced": "Refreshing",
        "Paranoia": "Jennerising",
        "Smelly": "Anti-Gravity",
        "Toxic": "Smelly",
    },
    "Chili": {
        "Anti-Gravity": "Tropic Thunder",
        "Athletic": "Euphoric",
        "Laxative": "Long Faced",
        "Munchies": "Toxic",
        "Shrinking": "Refreshing",
        "Sneaky": "Bright-Eyed",
    },
    "Iodine": {
        "Calming": "Balding",
        "Calorie-Dense": "Gingeritis",
        "Euphoric": "Seizure-Inducing",
        "Foggy": "Paranoia",
        "Refreshing": "Thought-Provoking",
        "Toxic": "Sneaky",
    },
    "Paracetamol": {
        "Calming": "Slippery",
        "Electrifying": "Athletic",
        "Energizing": "Paranoia",
        "Focused": "Gingeritis",
        "Foggy": "Calming",
        "Glowing": "Toxic",
        "Munchies": "Anti-Gravity",
        "Paranoia": "Balding",
        "Spicy": "Bright-Eyed",
        "Toxic": "Tropic Thunder",
    },
    "Viagor": {
        "Athletic": "Sneaky",
        "Disorienting": "Toxic",
        "Euphoric": "Bright-Eyed",
        "Laxative": "Calming",
        "Shrinking": "Gingeritis",
    },
    "Horse Semen": {
        "Anti-Gravity": "Calming",
        "Gingeritis": "Refreshing",
        "Seizure-Inducing": "Energizing",
        "Thought-Provoking": "Electrifying",
    },
    "Mega Bean": {
        "Athletic": "Laxative",
        "Calming": "Glowing",
        "Energizing": "Cyclopean",
        "Focused": "Disorienting",
        "Jennerising": "Paranoia",
        "Seizure-Inducing": "Focused",
        "Shrinking": "Electrifying",
        "Slippery": "Toxic",
        "Sneaky": "Calming",
        "Thought-Provoking": "Energizing",
    },
    "Addy": {
        "Explosive": "Euphoric",
        "Foggy": "Energizing",
        "Glowing": "Refreshing",
        "Long Faced": "Electrifying",
        "Sedating": "Gingeritis",
    },
    "Battery": {
        "Cyclopean": "Glowing",
        "Electrifying": "Euphoric",
        "Euphoric": "Zombifying",
        "Laxative": "Calorie-Dense",
        "Munchies": "Tropic Thunder",
        "Shrinking": "Munchies",
    },
}

# ——— Effect multipliers ———
MULTIPLIERS: Dict[str, float] = {
    "Anti-Gravity": 0.54,  "Athletic": 0.32,  "Balding": 0.30,
    "Bright-Eyed": 0.40,   "Calming": 0.10,   "Calorie-Dense": 0.28,
    "Cyclopean": 0.56,     "Disorienting": 0.00, "Electrifying": 0.50,
    "Energizing": 0.22,    "Euphoric": 0.18,   "Explosive": 0.00,
    "Focused": 0.16,       "Foggy": 0.36,      "Gingeritis": 0.20,
    "Glowing": 0.48,       "Jennerising": 0.42,"Laxative": 0.00,
    "Long Faced": 0.52,    "Munchies": 0.12,   "Paranoia": 0.00,
    "Refreshing": 0.14,    "Schizophrenia": 0.00, "Sedating": 0.26,
    "Seizure-Inducing": 0.00, "Shrinking": 0.60, "Slippery": 0.34,
    "Smelly": 0.00,        "Sneaky": 0.24,     "Spicy": 0.38,
    "Thought-Provoking": 0.44, "Toxic": 0.00,   "Tropic Thunder": 0.46,
    "Zombifying": 0.58,
}

# ——— Base drugs ———
BASE_DRUGS: Dict[str, Dict] = {
    "OG Kush":           {"price": 35.0, "effects": ["Calming"]},
    "Sour Diesel":       {"price": 35.0, "effects": ["Refreshing"]},
    "Green Crack":       {"price": 35.0, "effects": ["Energizing"]},
    "Granddaddy Purple": {"price": 35.0, "effects": ["Sedating"]},
    "Meth":              {"price": 70.0, "effects": []},
    "Cocaine":           {"price": 150.0, "effects": []},
}


# ——— Ingredient info ———
INGREDIENTS_INFO: Dict[str, Dict] = {
    "Cuke":          {"price": 2.0, "default": "Energizing"},
    "Banana":        {"price": 2.0, "default": "Gingeritis"},
    "Paracetamol":   {"price": 3.0, "default": "Sneaky"},
    "Donut":         {"price": 3.0, "default": "Calorie-Dense"},
    "Viagor":        {"price": 4.0, "default": "Tropic Thunder"},
    "Mouth Wash":    {"price": 4.0, "default": "Balding"},
    "Flu Medicine":  {"price": 5.0, "default": "Sedating"},
    "Gasoline":      {"price": 5.0, "default": "Toxic"},
    "Energy Drink":  {"price": 6.0, "default": "Athletic"},
    "Motor Oil":     {"price": 6.0, "default": "Slippery"},
    "Mega Bean":     {"price": 7.0, "default": "Foggy"},
    "Chili":         {"price": 7.0, "default": "Spicy"},
    "Battery":       {"price": 8.0, "default": "Bright-Eyed"},
    "Iodine":        {"price": 8.0, "default": "Jennerising"},
    "Addy":          {"price": 9.0, "default": "Thought-Provoking"},
    "Horse Semen":   {"price": 9.0, "default": "Long Faced"},
}

def apply_ingredient(effects: Set[str], ingr: str) -> Set[str]:
    effects.add(INGREDIENTS_INFO[ingr]["default"])
    for trig, repl in INTERACTIONS.get(ingr, {}).items():
        if trig in effects:
            effects.remove(trig)
            effects.add(repl)
    return effects


def compute_multiplier(effects: Set[str]) -> float:
    return sum(MULTIPLIERS.get(e, 0.0) for e in effects)


def calc_combo(combo: List[str], base_effects: List[str], base_price: float) -> Dict[str, any]:
    effects = set(base_effects)
    for ingr in combo:
        if ingr not in INGREDIENTS_INFO:
            raise ValueError(f"Unknown ingredient: {ingr}")
        effects = apply_ingredient(effects, ingr)

    total_mult = compute_multiplier(effects)
    final_price = base_price * (1 + total_mult)
    cost        = sum(INGREDIENTS_INFO[i]["price"] for i in combo)
    profit      = final_price - cost

    return {
        "effects": effects,
        "multiplier": total_mult,
        "final_price": round(final_price, 2),
        "cost": round(cost, 2),
        "profit": round(profit, 2)
    }


def find_best_mixtures(
    num_ings: int,
    base_effects: List[str],
    base_price: float
) -> List[Tuple[Tuple[str, ...], Dict[str, any]]]:
    """
    Returns a list of (combo, results) tuples for the most profitable mixtures.
    Supports multi-use (repetition) via combinations_with_replacement.
    """
    best_profit = float("-inf")
    best_list: List[Tuple[Tuple[str, ...], Dict[str, any]]] = []

    for combo in itertools.combinations_with_replacement(INGREDIENTS_INFO.keys(), num_ings):
        res = calc_combo(list(combo), base_effects, base_price)
        if res["profit"] > best_profit:
            best_profit = res["profit"]
            best_list = [(combo, res)]
        elif res["profit"] == best_profit:
            best_list.append((combo, res))
    return best_list


def main():
    p = argparse.ArgumentParser(description="Mixture profit calculator.")
    p.add_argument(
        "num_ingredients", type=int, nargs="?",
        help="# of ingredients to auto-search (ignored in manual mode)."
    )
    p.add_argument(
        "--base-drug", required=True,
        choices=list(BASE_DRUGS.keys()),
        help="Choose your base drug."
    )
    p.add_argument(
        "--ingredients",
        help="Comma-separated list of ingredients to apply in order (manual mode)."
    )
    args = p.parse_args()

    base = BASE_DRUGS[args.base_drug]
    print(f"\nBase drug: {args.base_drug}"
          f" (${base['price']:.2f}, effects={base['effects']})\n")

    if args.ingredients:
        combo = [i.strip() for i in args.ingredients.split(",")]
        res = calc_combo(combo, base["effects"], base["price"])
        print(f"Manual combo: {combo}")
        print(f" • Effects: {','.join(sorted(res['effects']))}")
        print(f" • Total multiplier: x{res['multiplier']:.2f}")
        print(f" • Final price: ${res['final_price']}")
        print(f" • Ingredient cost: ${res['cost']}")
        print(f" • Profit: ${res['profit']}\n")
    else:
        if args.num_ingredients is None:
            p.error("Either num_ingredients or --ingredients must be provided.")
        best = find_best_mixtures(
            args.num_ingredients, base['effects'], base['price']
        )
        print(f"=== Best mixtures with {args.num_ingredients} ingredients ===\n")
        for combo, res in best:
            print(f" • Combo: {combo}")
            print(f"   → Effects: {','.join(sorted(res['effects']))}")
            print(f"   → Total multiplier: x{res['multiplier']:.2f}")
            print(f"   → Final price: ${res['final_price']}")
            print(f"   → Ingredient cost: ${res['cost']}")
            print(f"   → Profit: ${res['profit']}\n")

if __name__ == "__main__":
    main()
