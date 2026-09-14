import unittest
import numpy as np
from nn_example_combinations import convex_weight


class CombinationTests(unittest.TestCase):
    def test_weaker_forecast_can_improve_combination(self):
        y = np.zeros(2)
        har = np.ones(2)
        neural = np.array([-2., 0.])
        self.assertGreater(np.mean((neural-y)**2), np.mean((har-y)**2))
        weight = convex_weight(y, har, neural)
        self.assertAlmostEqual(weight, .4)
        loss = np.mean(((1-weight)*har+weight*neural-y)**2)
        self.assertAlmostEqual(loss, .2)
        grid = np.linspace(0, 1, 1001)
        grid_loss = np.mean(((1-grid[:, None])*har+grid[:, None]*neural-y)**2, axis=1)
        self.assertLessEqual(loss, grid_loss.min()+1e-12)

    def test_constraints_can_select_either_component(self):
        har, neural = np.array([0., 1.]), np.array([1., 2.])
        self.assertEqual(convex_weight(har-1, har, neural), 0.)
        self.assertEqual(convex_weight(neural+1, har, neural), 1.)

    def test_identical_forecasts_retain_har(self):
        self.assertEqual(convex_weight([2., 4.], [1., 3.], [1., 3.]), 0.)

    def test_rejects_misaligned_or_nonfinite_vectors(self):
        with self.assertRaises(ValueError):
            convex_weight([1., 2.], [1.], [1., 2.])
        with self.assertRaises(ValueError):
            convex_weight([1., np.nan], [1., 2.], [1., 3.])


if __name__ == "__main__":
    unittest.main()
