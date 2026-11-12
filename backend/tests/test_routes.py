import asyncio
import unittest

from pydantic import ValidationError
from app.api.routes import (
    BridgeAnalysisInput,
    ScenarioInput,
    TrafficSimulationInput,
    analyze_scenario,
    calculate_bridge_necessity,
    haversine_km,
)


class RouteValidationTests(unittest.TestCase):
    def test_traffic_hour_must_be_in_24_hour_range(self):
        with self.assertRaises(ValidationError):
            TrafficSimulationInput(hour=24)
        with self.assertRaises(ValidationError):
            TrafficSimulationInput(hour=-1)

    def test_scenario_requires_two_valid_coordinates(self):
        with self.assertRaises(ValidationError):
            ScenarioInput(name="Road", type="road", coordinates=[[73.7, 18.5]])
        with self.assertRaises(ValidationError):
            ScenarioInput(name="Road", type="road", coordinates=[[190, 18.5], [73.8, 18.6]])

    def test_bridge_analysis_rejects_out_of_range_coordinates(self):
        with self.assertRaises(ValidationError):
            BridgeAnalysisInput(start_coords=[200, 18.5], end_coords=[73.8, 18.6], bridge_type="bridge")

    def test_haversine_uses_geodesic_distance(self):
        distance = haversine_km([0, 0], [1, 0])
        self.assertAlmostEqual(distance, 111.195, delta=0.2)

    def test_bridge_score_is_not_fabricated(self):
        request = BridgeAnalysisInput(
            start_coords=[73.7, 18.5],
            end_coords=[73.8, 18.6],
            bridge_type="bridge",
        )
        result = asyncio.run(calculate_bridge_necessity(request))
        self.assertEqual(result["analysisStatus"], "unavailable")
        self.assertIsNone(result["score"])
        self.assertIsNone(result["confidence"])

    def test_scenario_estimate_is_deterministic_and_labeled(self):
        request = ScenarioInput(
            name="Test Road",
            type="road",
            coordinates=[[73.7, 18.5], [73.8, 18.6]],
        )
        first = asyncio.run(analyze_scenario(request))
        second = asyncio.run(analyze_scenario(request))
        self.assertEqual(first["scenario_id"], second["scenario_id"])
        self.assertEqual(first["dataMode"], "illustrative_demo")


if __name__ == "__main__":
    unittest.main()