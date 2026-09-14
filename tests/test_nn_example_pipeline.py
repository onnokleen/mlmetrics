"""Temporal and scoring checks for the annual sliding-window illustration."""
import unittest
import numpy as np
import pandas as pd
import nn_example_pipeline as p


class ForecastProtocolTests(unittest.TestCase):
    def setUp(self):
        dates = pd.bdate_range("2015-01-02", "2024-12-31")
        rng = np.random.default_rng(7)
        values = np.exp(.3*np.sin(np.arange(len(dates))/40)+rng.normal(0,.2,len(dates)))
        self.data = pd.DataFrame({"date":dates,"rv":values})
        self.panel = p.make_inputs(self.data)

    def test_input_ends_before_target(self):
        positions = self.panel["target_positions"]
        np.testing.assert_array_equal(self.panel["lag_rv"][:, -1], self.data.rv.iloc[positions-1])
        np.testing.assert_array_equal(self.panel["lag_rv"][:, 0], self.data.rv.iloc[positions-756])
        np.testing.assert_array_equal(self.panel["y_rv"], self.data.rv.iloc[positions])
        self.assertEqual(self.panel["lag_rv"].shape[1],756)

    def test_architecture_specific_inputs(self):
        for target in p.TARGETS:
            expected = self.panel["lag_log" if target == "log(rv)" else "lag_rv"]
            for model, width in [("FNN",22),("Simple RNN",756),("LSTM",756),("HAR-FNN",3),("HAR-OLS",3)]:
                X, y = p.arrays_for(self.panel, model, target)
                self.assertEqual(X.shape[1], width)
                if model == "FNN":
                    np.testing.assert_array_equal(X,expected[:, -22:])
                self.assertEqual(len(y),len(self.panel["dates"]))

    def test_validation_and_test_cover_separate_calendar_years(self):
        dates = self.panel["dates"]
        validation = dates[(dates >= p.VALIDATION_START) & (dates < p.TEST_START)]
        test = dates[dates >= p.TEST_START]
        self.assertEqual(p.VALIDATION_START, pd.Timestamp("2022-01-01"))
        self.assertEqual(p.TEST_START, pd.Timestamp("2023-01-01"))
        self.assertEqual(set(validation.dt.year), {2022})
        self.assertEqual(set(test.dt.year), {2023, 2024})
        self.assertEqual(len(validation), sum(dates.dt.year == 2022))
        self.assertEqual(len(test), sum(dates.dt.year.isin([2023, 2024])))
        self.assertTrue(set(validation).isdisjoint(set(test)))
        for year in [2022, 2023, 2024]:
            first = dates[dates.dt.year == year].iloc[0]
            training = dates.iloc[p.estimation_indices(dates, first)]
            self.assertEqual(len(training), 756)
            self.assertLess(training.iloc[-1], pd.Timestamp(year=year, month=1, day=1))

    def test_sliding_window_drops_old_examples(self):
        dates=self.panel["dates"]
        first=p.estimation_indices(dates,p.TEST_START)
        second=p.estimation_indices(dates,pd.Timestamp("2024-01-02"))
        self.assertEqual(len(first),756)
        self.assertEqual(len(second),756)
        self.assertGreater(second[0],first[0])
        self.assertLess(dates.iloc[second[-1]],pd.Timestamp("2024-01-02"))

    def test_future_changes_cannot_affect_previous_year(self):
        _, predictions, records=p.annual_forecasts(self.panel,"HAR-OLS","log(rv)",None)
        altered=self.data.copy()
        altered.loc[altered.date>=pd.Timestamp("2024-01-01"),"rv"] *= 100
        _, changed, _=p.annual_forecasts(p.make_inputs(altered),"HAR-OLS","log(rv)",None)
        old=pd.DataFrame(predictions); new=pd.DataFrame(changed)
        previous=old.date.str.startswith("2023")
        np.testing.assert_array_equal(old.loc[previous,"forecast_rv"],new.loc[previous,"forecast_rv"])
        self.assertEqual([r["year"] for r in records],[2023,2024])
        self.assertTrue(all(r["estimation_examples"]==756 for r in records))

    def test_nonpositive_forecasts_are_not_clipped_into_log_losses(self):
        result=p.score_forecasts(np.array([1.,2.]),np.array([1.,-1.]))
        self.assertIsNone(result["rmse_log_rv"])
        self.assertIsNone(result["qlike"])
        self.assertEqual(result["nonpositive_rv_forecasts"],1)
        self.assertAlmostEqual(result["rmse_rv"],3/np.sqrt(2))


if __name__=="__main__":
    unittest.main()
