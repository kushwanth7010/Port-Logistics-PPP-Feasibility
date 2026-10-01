import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.port_model import evaluate, load_assumptions, CRORE

class PortModelTests(unittest.TestCase):
    def test_irr_npv_match_base_case(self):
        _, k, _ = evaluate()
        self.assertAlmostEqual(k["project_irr"],0.1278,delta=0.002)
        self.assertAlmostEqual(k["npv_inr_crore"],44.3865,delta=.01)
    def test_year_one_revenue_identity(self):
        df,k,_ = evaluate()
        a = load_assumptions()
        self.assertAlmostEqual(df.iloc[0]["revenue_inr_crore"],df.iloc[0]["processed_tonnes"]*a["realized_tariff_inr_per_tonne"]/CRORE)
        self.assertLessEqual(df["capacity_utilization"].max(),1.0)
    def test_cashflow_valuation(self):
        df,k,flows=evaluate()
        manual_npv=sum(x/((1+k["discount_rate"])**i) for i,x in enumerate(flows))/CRORE
        self.assertAlmostEqual(manual_npv,k["npv_inr_crore"], places=7)
        self.assertEqual(len(flows),21)
    def test_downside_has_lower_value(self):
        _,b,_=evaluate()
        _,d,_=evaluate({"traffic_capture_share":.14,"realized_tariff_inr_per_tonne":600,"initial_capex_inr_crore":770,"annual_market_growth":.03})
        self.assertLess(d["npv_inr_crore"],b["npv_inr_crore"])
    def test_reject_invalid_share(self):
        with self.assertRaises(ValueError): evaluate({"traffic_capture_share":1.1})

if __name__ == "__main__": unittest.main()
