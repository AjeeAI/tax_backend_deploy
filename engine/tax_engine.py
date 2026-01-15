# tax_engine.py

from .tax_rules_2024 import calculate_pita_2024
from .tax_rules_2026 import calculate_pita_2026


def calculate_tax_impact(monthly_income: float) -> dict:
    zero_tax_result = {
        "gross_income": annual_income,
        "taxable_income": 0.0,
        "consolidated_relief": 0.0,
        "annual_tax": 0.0,
        "monthly_tax": 0.0,
        "effective_rate": 0.0
    }
    annual_income = monthly_income * 12
    if annual_income > 800000:
        current = calculate_pita_2024(annual_income)
        proposed = calculate_pita_2026(annual_income)

        annual_relief = current["annual_tax"] - proposed["annual_tax"]
        monthly_relief = annual_relief / 12

        percentage_change = (
            (annual_relief / current["annual_tax"]) * 100
            if current["annual_tax"] > 0 else 0
        )

        return {
            "monthly_income": monthly_income,
            "annual_income": annual_income,

            "current": {
                "label": "2024 PITA",
                **current
            },

            "proposed": {
                "label": "2026 Reform",
                **proposed
            },

            "impact": {
                "monthly_relief": round(monthly_relief, 2),
                "annual_relief": round(annual_relief, 2),
                "percentage_change": round(percentage_change, 2)
            }
        }
    
    else:
        # 2. Use the zero template for low earners (Exempt)
        current = zero_tax_result
        proposed = zero_tax_result
        
        annual_relief = 0.0
        monthly_relief = 0.0
        percentage_change = 0.0

    # 3. Unified return statement
    # We return the exact same structure regardless of income level
    return {
        "monthly_income": monthly_income,
        "annual_income": annual_income,

        "current": {
            "label": "2024 PITA",
            **current
        },

        "proposed": {
            "label": "2026 Reform",
            **proposed
        },

        "impact": {
            "monthly_relief": round(monthly_relief, 2),
            "annual_relief": round(annual_relief, 2),
            "percentage_change": round(percentage_change, 2)
        }
    }
