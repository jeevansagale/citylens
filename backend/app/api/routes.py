from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from math import asin, cos, radians, sin, sqrt

router = APIRouter()

# ============ Models ============

class ScenarioInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: Literal["bridge", "flyover", "tunnel", "road"]
    coordinates: List[List[float]] = Field(min_length=2, max_length=500)  # [[lng, lat], ...]

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, coordinates):
        for point in coordinates:
            if len(point) != 2:
                raise ValueError("Each coordinate must contain longitude and latitude")
            longitude, latitude = point
            if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
                raise ValueError("Coordinate is outside valid longitude/latitude bounds")
        return coordinates

class TrafficSimulationInput(BaseModel):
    hour: int = Field(ge=0, le=23)
    scenario_id: Optional[str] = None

class BridgeAnalysisInput(BaseModel):
    start_coords: tuple[float, float]  # [lng, lat]
    end_coords: tuple[float, float]    # [lng, lat]
    bridge_type: Literal["bridge", "flyover", "tunnel"]

    @field_validator("start_coords", "end_coords")
    @classmethod
    def validate_point(cls, point):
        longitude, latitude = point
        if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
            raise ValueError("Coordinate is outside valid longitude/latitude bounds")
        return point

def haversine_km(start: List[float], end: List[float]) -> float:
    """Calculate geodesic distance between [longitude, latitude] points."""
    lon1, lat1 = radians(start[0]), radians(start[1])
    lon2, lat2 = radians(end[0]), radians(end[1])
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    value = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 6371.0088 * 2 * asin(sqrt(min(1.0, max(0.0, value))))

# ============ Traffic Data ============

@router.get("/traffic/current")
async def get_current_traffic():
    """Get current traffic data for all road segments"""
    return {
        "dataMode": "demo",
        "dataNotice": "Static demonstration fixture; not live or verified traffic data.",
        "timestamp": "2026-04-07T11:00:00",
        "segments": [
            {
                "id": "road-1",
                "name": "Mumbai-Bangalore Highway (NH48)",
                "trafficDensity": 0.85,
                "currentSpeed": 25,
                "avgWaitTime": 12
            },
            {
                "id": "road-2", 
                "name": "Wakad-Hinjewadi Road",
                "trafficDensity": 0.92,
                "currentSpeed": 15,
                "avgWaitTime": 22
            },
            {
                "id": "road-3",
                "name": "Dange Chowk Road",
                "trafficDensity": 0.65,
                "currentSpeed": 30,
                "avgWaitTime": 8
            }
        ],
        "overallCongestionIndex": 78
    }

@router.post("/traffic/simulate")
async def simulate_traffic(input: TrafficSimulationInput):
    """Simulate traffic for a specific hour"""
    # Peak hour multipliers
    multiplier = 1.0
    if 8 <= input.hour <= 11:
        multiplier = 2.5
    elif 17 <= input.hour <= 21:
        multiplier = 2.8
    
    base_density = 0.35
    simulated_density = min(1.0, base_density * multiplier)
    
    return {
        "dataMode": "illustrative_demo",
        "assumptions": "Fixed peak-hour multipliers; not calibrated to measured traffic.",
        "hour": input.hour,
        "isPeakHour": 8 <= input.hour <= 11 or 17 <= input.hour <= 21,
        "trafficMultiplier": multiplier,
        "estimatedDensity": simulated_density,
        "estimatedVehicles": int(3500 * multiplier),
        "avgTravelTime": int(10 * multiplier),
    }

# ============ Scenario Analysis ============

@router.post("/scenario/analyze")
async def analyze_scenario(scenario: ScenarioInput):
    """Analyze impact of a proposed infrastructure scenario"""
    # Mock analysis - in production, this would run SUMO or similar
    
    # Calculate mock impact based on scenario type
    impact_factors = {
        'flyover': {'time_reduction': 0.58, 'cost_per_km': 150},  # Crores per km
        'bridge': {'time_reduction': 0.35, 'cost_per_km': 80},
        'tunnel': {'time_reduction': 0.72, 'cost_per_km': 300},
        'road': {'time_reduction': 0.20, 'cost_per_km': 25}
    }
    
    factors = impact_factors.get(scenario.type, impact_factors['road'])
    
    # Use geodesic distance rather than degree-space Euclidean distance.
    coords = scenario.coordinates
    dist = sum(haversine_km(coords[i], coords[i + 1]) for i in range(len(coords) - 1))
    
    estimated_cost = dist * factors['cost_per_km']
    time_reduction = factors['time_reduction'] * 100
    
    return {
        "scenario_id": f"demo-{scenario.type}-{round(dist, 3)}",
        "dataMode": "illustrative_demo",
        "assumptions": "Fixed demonstration cost and impact factors; not validated against a transport model.",
        "name": scenario.name,
        "type": scenario.type,
        "analysis": {
            "estimatedLength": round(dist, 2),
            "estimatedCost": round(estimated_cost, 2),  # Crores
            "travelTimeReduction": round(time_reduction, 1),  # Percentage
            "congestionReduction": round(time_reduction * 0.7, 1),
            "constructionTime": int(dist * 6),  # Months
            "vehiclesPerDayBenefit": int(285000 * factors['time_reduction'])
        },
        "beforeMetrics": {
            "avgTravelTime": 22,
            "congestionIndex": 78
        },
        "afterMetrics": {
            "avgTravelTime": round(22 * (1 - factors['time_reduction']), 1),
            "congestionIndex": round(78 * (1 - factors['time_reduction'] * 0.7))
        }
    }

# ============ AI/ML Endpoints ============

@router.post("/ai/bridge-necessity-score")
async def calculate_bridge_necessity(input: BridgeAnalysisInput):
    """Return an explicit unavailable status until validated data and a model exist."""
    distance_km = haversine_km(list(input.start_coords), list(input.end_coords))
    return {
        "analysisStatus": "unavailable",
        "dataMode": "not_connected",
        "score": None,
        "recommendation": "Not evaluated",
        "confidence": None,
        "distanceKm": round(distance_km, 3),
        "interventionType": input.bridge_type,
        "reason": "No validated traffic, route-capacity, population or accident dataset and no evaluated ML model are connected.",
    }

@router.post("/ai/diversion-impact")
async def predict_diversion_impact(scenario: ScenarioInput):
    """Report that diversion analysis is unavailable without a traffic assignment model."""
    return {
        "analysisStatus": "unavailable",
        "dataMode": "not_connected",
        "scenario": scenario.name,
        "message": "No validated road-network and traffic-assignment model is connected; route-level diversion impacts are not estimated.",
    }

# ============ Government Data ============

@router.get("/govt/projects")
async def get_govt_projects():
    """Get ongoing government infrastructure projects"""
    return {
        "dataMode": "demo",
        "dataNotice": "Illustrative project and hotspot fixtures; not verified government records.",
        "pwd": {
            "name": "Public Works Department",
            "projects": [
                {"id": "pwd-1", "name": "Road widening near Wakad", "status": "ongoing", "completion": 65},
                {"id": "pwd-2", "name": "Drainage repair Hinjewadi", "status": "planned", "completion": 0},
                {"id": "pwd-3", "name": "Footpath construction", "status": "completed", "completion": 100}
            ]
        },
        "traffic": {
            "name": "Traffic Police",
            "accidentHotspots": [
                {"location": [73.7625, 18.5987], "severity": "high", "incidents": 23},
                {"location": [73.7168, 18.5913], "severity": "medium", "incidents": 12}
            ],
            "signalTimings": [
                {"junction": "Wakad Chowk", "greenTime": 45, "redTime": 90},
                {"junction": "Hinjewadi Phase 1", "greenTime": 60, "redTime": 120}
            ]
        },
        "msrdc": {
            "name": "MSRDC",
            "projects": [
                {"id": "msrdc-1", "name": "NH48 Expansion", "status": "ongoing", "completion": 40}
            ]
        }
    }

# ============ Analytics ============

@router.get("/analytics/summary")
async def get_analytics_summary():
    """Get city-wide analytics summary"""
    return {
        "dataMode": "demo",
        "dataNotice": "Static demonstration metrics; not live measurements.",
        "currentMetrics": {
            "avgTravelTime": 22,
            "congestionIndex": 78,
            "accidentRate": 2.3,
            "airQualityIndex": 156,
            "dailyVehicles": 285000,
            "publicTransportShare": 18
        },
        "trends": {
            "travelTime": {"direction": "increasing", "change": 8},
            "congestion": {"direction": "increasing", "change": 12},
            "accidents": {"direction": "decreasing", "change": -5}
        },
        "peakHours": {
            "morning": {"start": 8, "end": 11, "severity": "high"},
            "evening": {"start": 17, "end": 21, "severity": "critical"}
        }
    }
