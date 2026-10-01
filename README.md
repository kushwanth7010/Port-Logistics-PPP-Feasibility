# Port & Logistics Infrastructure Feasibility and PPP Advisory

**Consulting portfolio case · Python · NPV/IRR · 20-year discounted cash-flow valuation · scenarios · PPP risk assessment**

This is a **hypothetical, independently built case study** with illustrative financial inputs—not a client engagement, investment recommendation, or analysis of a named Indian port.

## Business question
Should a proposed port and logistics terminal advance to detailed feasibility and possible public–private partnership procurement?

## Included model
- Twenty-year forecast with addressable cargo demand, capture share, and a terminal capacity ceiling.
- Revenue, operating costs, EBITDA, simplified tax, and unlevered project free cash flow.
- Project IRR, correctly timed Year-0-to-Year-20 NPV, payback, three scenarios, and input sensitivities.
- Diligence recommendations for cargo validation, competition, connectivity, permits, capex, and PPP risk allocation.

### Base-case assumptions
Year 1 market: 12 million tonnes; growth: 6%; capture: 18%; terminal capacity: 7.5 million tonnes; tariff: INR 650/tonne; initial capex: INR 700 crore; fixed operating cost: INR 30 crore annually; variable operating cost: INR 180/tonne; discount rate: 12%; tax assumption: 25%; concession: 20 years.

**Base-case results:** IRR ~12.78%; NPV ~INR 44.39 crore at 12%. All figures are hypothetical.

## Run
```bash
python -m pip install -r requirements.txt
python -m src.port_model
python -m unittest discover -s tests -v
```

Edit `data/assumptions.json` and rerun to explore the financial implications. Calculated results are saved to `outputs/`.

**Consulting conclusion:** advance to diligence rather than grant unconditional investment approval; independently validate actual cargo volumes, tariff realization, land/connectivity, approvals, capex, financeability and risk allocation.

**Portfolio purpose:** practice financial feasibility, structured problem solving, scenarios, project risk and evidence-based investment recommendations.
