"""Illustrative, unlevered port-terminal project valuation. INR, crore=10 million."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import numpy_financial as npf
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CRORE = 10_000_000


def load_assumptions(path=ROOT / "data" / "assumptions.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(a):
    for key in ("initial_addressable_market_tonnes", "annual_terminal_capacity_tonnes", "realized_tariff_inr_per_tonne", "initial_capex_inr_crore", "concession_years"):
        if float(a[key]) <= 0:
            raise ValueError(f"{key} must be positive")
    for key in ("annual_market_growth", "traffic_capture_share", "discount_rate", "corporate_tax_rate"):
        if not (0 <= float(a[key]) < 1):
            raise ValueError(f"{key} must be in [0,1)")
    if int(a["concession_years"]) != a["concession_years"]:
        raise ValueError("concession_years must be an integer")
    if float(a["realized_tariff_inr_per_tonne"]) <= float(a["variable_opex_inr_per_tonne"]):
        raise ValueError("tariff must exceed variable opex for operating breakeven")


def evaluate(overrides=None):
    a = load_assumptions()
    if overrides:
        a.update(overrides)
    validate(a)
    initial_capex = a["initial_capex_inr_crore"] * CRORE
    depreciation = initial_capex / a["concession_years"]
    yearly_cashflows = [-initial_capex]
    rows = []
    for y in range(1, int(a["concession_years"]) + 1):
        market_t = a["initial_addressable_market_tonnes"] * (1 + a["annual_market_growth"])**(y - 1)
        demand_t = market_t * a["traffic_capture_share"]
        processed_t = min(demand_t, a["annual_terminal_capacity_tonnes"])
        revenue = processed_t * a["realized_tariff_inr_per_tonne"]
        variable_cost = processed_t * a["variable_opex_inr_per_tonne"]
        fixed_cost = a["annual_fixed_opex_inr_crore"] * CRORE
        ebitda = revenue - variable_cost - fixed_cost
        ebit = ebitda - depreciation
        tax = max(ebit, 0) * a["corporate_tax_rate"]  # simplified: no tax-loss carryforward
        residual = a["terminal_residual_value_inr_crore"] * CRORE if y == a["concession_years"] else 0
        delta_wc = a["working_capital_change_inr_crore_per_year"] * CRORE
        free_cashflow = ebitda - tax - delta_wc + residual
        yearly_cashflows.append(free_cashflow)
        rows.append({
            "year": y, "addressable_market_tonnes": round(market_t),
            "unconstrained_demand_tonnes": round(demand_t), "processed_tonnes": round(processed_t),
            "capacity_utilization": processed_t / a["annual_terminal_capacity_tonnes"],
            "revenue_inr_crore": revenue / CRORE, "variable_opex_inr_crore": variable_cost / CRORE,
            "fixed_opex_inr_crore": fixed_cost / CRORE, "ebitda_inr_crore": ebitda / CRORE,
            "depreciation_inr_crore": depreciation / CRORE, "ebit_inr_crore": ebit / CRORE,
            "tax_inr_crore": tax / CRORE, "project_fcf_inr_crore": free_cashflow / CRORE,
            "discounted_fcf_inr_crore": (free_cashflow / CRORE) / ((1+a["discount_rate"])**y)
        })
    npv_crore = npf.npv(a["discount_rate"], yearly_cashflows)/CRORE
    irr = npf.irr(yearly_cashflows)
    simple_payback = None
    cumulative = -initial_capex
    for year, cf in enumerate(yearly_cashflows[1:], start=1):
        old = cumulative
        cumulative += cf
        if cumulative >= 0 and simple_payback is None:
            simple_payback = (year-1) + (-old/cf)
    metrics = {
        "project_irr": float(irr), "npv_inr_crore": float(npv_crore),
        "year_1_revenue_inr_crore": rows[0]["revenue_inr_crore"],
        "year_1_ebitda_inr_crore": rows[0]["ebitda_inr_crore"],
        "year_1_processed_tonnes": rows[0]["processed_tonnes"],
        "ebitda_breakeven_tonnes": a["annual_fixed_opex_inr_crore"] * CRORE/(a["realized_tariff_inr_per_tonne"]-a["variable_opex_inr_per_tonne"]),
        "simple_payback_years": simple_payback,
        "discount_rate": a["discount_rate"]
    }
    return pd.DataFrame(rows), metrics, yearly_cashflows


def generate_reports():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)
    a = load_assumptions()
    cash, main, flows = evaluate()
    cash.to_csv(output / "base_case_annual_cashflows.csv", index=False)
    (output / "base_case_kpis.json").write_text(json.dumps(main, indent=2), encoding="utf-8")
    scenario_inputs = {
        "Downside": {"annual_market_growth":.03, "traffic_capture_share":.14, "realized_tariff_inr_per_tonne":600, "initial_capex_inr_crore":770},
        "Base": {},
        "Upside": {"annual_market_growth":.08, "traffic_capture_share":.20, "realized_tariff_inr_per_tonne":700, "initial_capex_inr_crore":665},
    }
    scenarios = []
    for name, inputs in scenario_inputs.items():
        _, kpi, _ = evaluate(inputs)
        scenarios.append({"scenario":name, "growth":inputs.get("annual_market_growth",a["annual_market_growth"]),
                          "capture_share":inputs.get("traffic_capture_share",a["traffic_capture_share"]),
                          "tariff_inr_per_tonne":inputs.get("realized_tariff_inr_per_tonne",a["realized_tariff_inr_per_tonne"]),
                          "capex_inr_crore":inputs.get("initial_capex_inr_crore",a["initial_capex_inr_crore"]),
                          "project_irr":kpi["project_irr"], "npv_inr_crore":kpi["npv_inr_crore"]})
    scenario_df = pd.DataFrame(scenarios)
    scenario_df.to_csv(output/"scenario_comparison.csv", index=False)
    sensitivities = []
    for key in ("traffic_capture_share", "realized_tariff_inr_per_tonne", "initial_capex_inr_crore", "annual_fixed_opex_inr_crore", "variable_opex_inr_per_tonne"):
        for delta in (-.10,.10):
            _, kpi, _ = evaluate({key: a[key]*(1+delta)})
            sensitivities.append({"input":key,"change_pct":delta,"npv_inr_crore":kpi["npv_inr_crore"],
                                  "project_irr":kpi["project_irr"]})
    pd.DataFrame(sensitivities).to_csv(output/"sensitivity_comparison.csv", index=False)
    plt.figure(figsize=(8,4.5))
    plt.bar(scenario_df["scenario"],scenario_df["npv_inr_crore"])
    plt.axhline(0, linewidth=1)
    plt.ylabel("Project NPV (INR crore)")
    plt.title("Project value under assumed scenarios")
    plt.tight_layout()
    plt.savefig(output/"scenario_npv.png",dpi=170)
    plt.close()
    plt.figure(figsize=(8,4.5))
    plt.plot(cash["year"], cash["revenue_inr_crore"], marker="o",label="Revenue")
    plt.plot(cash["year"],cash["ebitda_inr_crore"],marker="s",label="EBITDA")
    plt.xlabel("Concession year")
    plt.ylabel("INR crore")
    plt.title("Annual project operating economics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output/"revenue_ebitda.png",dpi=170)
    plt.close()
    print("BASE_CASE",json.dumps(main,indent=2))
    print("SCENARIOS\n",scenario_df.round(4).to_string(index=False))

if __name__ == "__main__":
    generate_reports()
