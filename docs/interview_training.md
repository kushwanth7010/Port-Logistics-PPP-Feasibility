# Port project | deep-dive learning and consulting interview defense

## A. Understand the problem first
A port authority is studying a logistics terminal. The **strategic question** is not merely “can I code a model?” It is “is this investment commercially sensible, and is it ready for a PPP procurement?” Separate the question into (1) market, (2) operating/technical, (3) financial, (4) transaction/risk and (5) implementation. The Python model tests the financial implications of **explicit assumptions**; it does not validate the assumptions themselves.

## B. Learn the exact data flow
`data/assumptions.json` → `src/port_model.py` → `outputs/base_case_annual_cashflows.csv` → NPV/IRR KPIs → `outputs/scenario_comparison.csv` → conditional recommendation.

Open the code in this order: `load_assumptions`, `validate`, `evaluate` (the annual loop), NPV/IRR block, `generate_reports`. You should be able to explain each function before an interview.

### A worked first-year example
- Addressable market = 12,000,000 tonnes.
- Capture = 18%, so unconstrained demand = 2,160,000 tonnes.
- Capacity = 7,500,000 tonnes, so processed volume stays 2,160,000.
- Tariff = INR 650; revenue = 2,160,000 × 650 = INR 1,404,000,000 = **INR 140.4 crore**.
- Variable cost = 2,160,000 × 180 = INR 388,800,000 = **INR 38.88 crore**.
- Fixed opex = INR 30 crore.
- EBITDA = 140.4 − 38.88 − 30 = **INR 71.52 crore**.
- Straight-line depreciation = INR 700 crore/20 = INR 35 crore/year.
- Taxable EBIT = 71.52 − 35 = INR 36.52 crore; simplified cash tax = 25% × 36.52 = **INR 9.13 crore**.
- First-year unlevered project FCF = EBITDA − cash tax = **INR 62.39 crore** (zero working-capital change, no debt or maintenance capex in this simplified case).

### What NPV and IRR mean
- **NPV** discounts the project's future free cash flows and subtracts initial capex. A positive NPV at the *assumed* discount rate means the modeled investment clears that particular financial hurdle **under the assumptions**.
- **IRR** is the discount rate at which the same project's NPV equals zero.
- **Project IRR** is based on unlevered cash flows. **Equity IRR** requires a full funding/debt model and cannot be quoted from this repository.
- **Payback** ignores the time value of money when presented as simple payback; do not confuse it with NPV.
- **EBITDA breakeven throughput** = fixed opex / (tariff − variable opex); it does not pay back initial capex.

## C. What each scenario tests
- **Downside:** 3% growth, 14% share, INR 600/tonne tariff, INR 770 crore capex.
- **Base:** 6% growth, 18% share, INR 650/tonne tariff, INR 700 crore capex.
- **Upside:** 8% growth, 20% share, INR 700/tonne tariff, INR 665 crore capex.

Run the code and read exact `outputs/scenario_comparison.csv`. Explain *why* scenarios differ: volume, tariff and capex all affect NPV; capacity limits some upside. You cannot infer scenario probability from this simulation.

## D. Recommendation (consulting style)
**Lead with the decision:** proceed to detailed feasibility only, not full approval. The base may satisfy the illustrative hurdle, but a traffic/tariff/capex downside can destroy value. Next validate independent demand, anchor customers, competing port economics, tariff willingness, land, road/rail evacuation, environmental approvals, capex and concession terms.

## E. Questions and ready reasoning
1. **Why this project?** It demonstrates structured consulting logic in infrastructure: market sizing, operational assumptions, financial feasibility, risks and a recommendation.
2. **What is a PPP?** A long-term arrangement where public and private parties allocate investment, obligations, performance and project risks under an agreed contract. Models differ by sector and concession design.
3. **What is a feasibility study?** A disciplined evaluation of demand, technical practicality, economic/financial viability, approvals, stakeholders and implementation risks.
4. **Why use 18% capture?** It is an invented assumption for a learning case. Real selection needs competitor throughput, service levels, customer interviews and cargo origin–destination data.
5. **Why limit throughput by capacity?** A forecast cannot exceed the asset's technical capacity without expansion capex.
6. **Why use project FCF instead of revenue?** Investment creates value from cash remaining after operating costs, tax, reinvestment and capital requirements, not headline sales.
7. **Why do depreciation and tax appear?** Depreciation reduces taxable EBIT even though it is non-cash; the model uses it only to determine simplified cash tax.
8. **Why discount future cash?** Later cash is less valuable/riskier relative to the present; the chosen 12% is a case hurdle assumption.
9. **Is 12% the actual WACC for an Indian port?** No. It is a case assumption, and a real project needs a defensible risk-adjusted discount rate.
10. **Why not invest immediately with positive NPV?** Assumptions are unvalidated and downside risks, approvals, funding and public value have not been assessed.
11. **Does positive NPV prove PPP suitability?** No. Compare procurement structures, value for money, risk transfer, affordability and public objectives.
12. **What is traffic risk?** Throughput and related revenue can be lower than planned because demand or competitive conditions change.
13. **Who bears traffic risk?** Depends on contract design; often the private partner in demand-based concessions, possibly shared or mitigated.
14. **What is transaction advisory?** Helping structure, appraise, procure, negotiate and close a transaction, subject to legal/financial mandates.
15. **What are the top project limitations?** No real market evidence, financing, phased construction, maintenance capex, inflation, regulatory tariff testing, tax-loss treatment or detailed environmental appraisal.
16. **What would you do next with real data?** Replace assumptions with observed cargo statistics, field research, customer demand estimates, technical layouts, capex quotes and financing terms.
17. **Why both IRR and NPV?** NPV measures absolute value at a defined hurdle; IRR is a percentage yield. Both help but may disagree between mutually exclusive projects.
18. **How would a 10% capex overrun affect the decision?** Recalculate initial cash outflow and NPV/IRR; compare with sensitivity outputs and identify required contingencies.
19. **How could you improve the model?** Model construction stages, annual tariff inflation, maintenance capex, debt amortization, DSCR, working capital, tax losses and alternative contract terms.
20. **What was your individual contribution?** Constructed and tested the standalone portfolio model, documented assumptions, generated scenarios and wrote a consulting-style recommendation.

## F. 45-second project presentation
“I developed a hypothetical port/logistics PPP feasibility case. I first structured the decision around cargo demand, capacity, tariffs, costs, capital expenditure and risk allocation. I built a 20-year unlevered project model, calculated annual cash flow, NPV and IRR, and tested downside, base and upside assumptions. I added a capacity constraint and sensitivity tests to avoid an overly optimistic volume forecast. The recommendation was to proceed only to detailed diligence until traffic, tariff, costs and regulatory requirements are verified. It is a synthetic case study, not real client advice.”

## G. Practice problems (solve before looking at formulas)
1. Calculate revenue at 3 million tonnes and INR 650/tonne. Answer: INR 195 crore.
2. Find EBITDA when revenue is INR 195 crore, variable opex INR 54 crore and fixed opex INR 30 crore. Answer: INR 111 crore.
3. If capex is INR 700 crore and depreciation is straight-line over 20 years with no salvage, find annual depreciation. Answer: INR 35 crore.
4. Find EBITDA breakeven throughput at INR 650 tariff, INR 180 variable opex and INR 30 crore fixed opex. Answer: ~638,298 tonnes/year.
5. Explain why an NPV-positive port may still be environmentally or socially unacceptable. (Financial value is not an environmental/social appraisal.)
