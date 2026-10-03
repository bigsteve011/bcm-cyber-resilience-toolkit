import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import bia_engine as bia  # noqa: E402


class BiaTests(unittest.TestCase):
    def test_mtpd_is_first_unacceptable_window(self):
        p = bia.Process("x", "o", {"financial": [1, 2, 4, 5, 5, 5], "customer": [1, 1, 1, 1, 1, 1]})
        self.assertEqual(p.mtpd_hours, 8)
        self.assertEqual(p.rto_hours, 4)
        self.assertEqual(p.tier, "Tier 1")

    def test_unacceptable_in_first_hour_halves_rto(self):
        p = bia.Process("x", "o", {"financial": [4, 5, 5, 5, 5, 5]})
        self.assertEqual(p.rto_hours, 0.5)

    def test_never_unacceptable_is_tier_3(self):
        p = bia.Process("x", "o", {"financial": [1, 1, 1, 2, 3, 3]})
        self.assertEqual(p.tier, "Tier 3")

    def test_sample_gaps(self):
        procs = {p.name: p for p in bia.load_bia()}
        caps = bia.load_capabilities()
        self.assertTrue(any("core-banking" in g for g in bia.gaps(procs["Payments processing"], caps)))
        self.assertEqual(bia.gaps(procs["Customer onboarding (KYC)"], caps), [])
        self.assertTrue(any("FAILED" in g for g in bia.gaps(procs["Treasury & liquidity reporting"], caps)))


if __name__ == "__main__":
    unittest.main()
