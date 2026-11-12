# CityLens — Urban Planning Digital Twin

A hackathon prototype for exploring urban infrastructure scenarios through an interactive city map, traffic visualization, and before/after comparisons.

The project was developed for Cresendo '26 at VIT. It focuses on a Wakad–Hinjewadi case study in Pune.

## Overview

CityLens brings together a map-based view of an urban area and a scenario workflow for sketching proposed infrastructure changes. Users can explore traffic layers, create a proposed intervention, and compare the displayed baseline and scenario metrics.

## Core Features

- Interactive map centered on the Wakad–Hinjewadi area.
- Traffic and road-network visualization.
- Scenario drawing for proposed infrastructure such as flyovers and bridges.
- Before/after scenario comparison.
- Analytics panel with a bridge-necessity score.
- Backend API for traffic, scenario, and analytics data.

## Important Data Disclaimer

This repository includes demonstration data and mock analysis. Values shown in the hackathon scenario—including traffic, congestion, cost, savings, and AI score—must not be treated as verified live traffic measurements, engineering estimates, or validated model predictions.

The current bridge-necessity score is a mock/demo score, not a trained and validated ML model. Government-data integration and live-data claims should be considered unverified unless supported by source documentation and operational API connections.

## Architecture

```text
Interactive Map and Scenario UI
             |
             v
         Backend API
             |
      +------+------+
      |             |
      v             v
 Traffic Data   Scenario Analysis
      |             |
      +------+------+
             |
             v
      Comparison Results
```

## Repository Structure

```text
citylens/
├── backend/       # FastAPI application and API routes
├── frontend/      # Interactive map and scenario interface
├── README.md
├── QUICKSTART.md
├── DEMO_GUIDE.md
└── TECH_STACK.md
```

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API documentation is available at `http://localhost:8000/docs` while the backend is running.

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Use the development URL printed by the frontend tooling. Configure any required map provider token using the local environment configuration; do not commit secrets.

## Documentation

- [Quick Start](QUICKSTART.md)
- [Demo Guide](DEMO_GUIDE.md)
- [Technical Stack](TECH_STACK.md)

## Project Status

This is a hackathon prototype. It demonstrates a map-based scenario workflow, but it is not a production urban-planning system and should not be used for infrastructure decisions without validated datasets, calibrated models, and domain review.

## License

No license file is currently included. Unless a license is added, the repository should be treated as source available for viewing, not as granting general permission to reuse or redistribute the code.
