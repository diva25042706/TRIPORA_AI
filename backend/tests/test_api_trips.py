import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.db.session import init_db

import uuid

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.mark.asyncio
async def test_api_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/health/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "LangGraph" in data["multi_agent_framework"]

@pytest.mark.asyncio
async def test_auth_and_trip_crud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        test_email = f"user_{uuid.uuid4().hex[:6]}@tripora.ai"
        # Register user
        reg_resp = await client.post("/api/v1/auth/register", json={
            "email": test_email,
            "password": "securepassword123",
            "full_name": "Test Explorer",
            "preferred_currency": "INR"
        })
        assert reg_resp.status_code == 200
        token = reg_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create trip
        trip_resp = await client.post("/api/v1/trips/", headers=headers, json={
            "title": "CRUD Test Trip to Jaipur",
            "origin": "Delhi",
            "destination": "Jaipur",
            "start_date": "2026-12-01",
            "end_date": "2026-12-03",
            "travellers": 2,
            "total_budget": 30000.0,
            "currency": "INR",
            "travel_style": "Balanced",
            "interests": ["Culture", "Food"],
            "accommodation_pref": "Hotel",
            "transport_pref": "Train"
        })
        assert trip_resp.status_code == 201
        trip_data = trip_resp.json()
        trip_id = trip_data["id"]
        assert trip_data["destination"] == "Jaipur"
        assert trip_data["full_trip_data"] is not None

        # Get trip
        get_resp = await client.get(f"/api/v1/trips/{trip_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == trip_id

        # List trips
        list_resp = await client.get("/api/v1/trips/", headers=headers)
        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 1

        # Replan trip
        replan_resp = await client.post(f"/api/v1/trips/{trip_id}/replan", headers=headers, json={
            "instruction": "Rain predicted on Day 2, swap outdoor activities for indoor museums",
            "new_travel_style": "Relaxed"
        })
        assert replan_resp.status_code == 200
        replan_data = replan_resp.json()
        assert "diff_summary" in replan_data
        assert len(replan_data["diff_summary"]["changes_summary"]) > 0

        # Chat regarding trip
        chat_resp = await client.post(f"/api/v1/chat/{trip_id}/message", headers=headers, json={
            "message": "What is the total estimated budget and can you summarize Day 1?"
        })
        assert chat_resp.status_code == 200
        assert "content" in chat_resp.json()

        # Delete trip
        del_resp = await client.delete(f"/api/v1/trips/{trip_id}", headers=headers)
        assert del_resp.status_code == 204
