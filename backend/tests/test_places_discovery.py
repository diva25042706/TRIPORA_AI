import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.providers.chennai_places_data import CHENNAI_COMPREHENSIVE_PLACES
from app.providers.geo_places_provider import DESTINATION_CATALOG

@pytest.mark.asyncio
async def test_places_discovery_removes_three_result_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/places/search?limit=50")
        assert response.status_code == 200
        data = response.json()
        
        # Verify result count is substantially greater than the previous 3-result limitation
        assert data["total"] >= 50
        assert len(data["results"]) >= 50
        assert data["page"] == 1
        assert "available_categories" in data
        assert len(data["available_categories"]) >= 10
        assert "available_zones" in data
        assert len(data["available_zones"]) == 3

@pytest.mark.asyncio
async def test_places_discovery_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Page 1 with limit 10
        resp1 = await ac.get("/api/v1/places/search?page=1&limit=10")
        assert resp1.status_code == 200
        d1 = resp1.json()
        assert len(d1["results"]) == 10
        assert d1["has_more"] is True
        assert d1["total_pages"] >= 5

        # Page 2 with limit 10
        resp2 = await ac.get("/api/v1/places/search?page=2&limit=10")
        assert resp2.status_code == 200
        d2 = resp2.json()
        assert len(d2["results"]) == 10
        
        # Ensure page 1 and page 2 results are distinct
        ids_page1 = {p["id"] for p in d1["results"]}
        ids_page2 = {p["id"] for p in d2["results"]}
        assert len(ids_page1.intersection(ids_page2)) == 0

@pytest.mark.asyncio
async def test_places_discovery_category_filter():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/places/search?category=Beaches %26 Waterfronts")
        assert resp.status_code == 200
        d = resp.json()
        assert d["total"] >= 5
        for item in d["results"]:
            assert item["category"] == "Beaches & Waterfronts"

@pytest.mark.asyncio
async def test_places_discovery_area_zone_separation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. City places
        resp_city = await ac.get("/api/v1/places/search?area_zone=chennai_city&limit=100")
        assert resp_city.status_code == 200
        d_city = resp_city.json()
        assert d_city["total"] >= 35
        for p in d_city["results"]:
            assert p["area_zone"] == "chennai_city"

        # 2. Day trips outside Chennai
        resp_daytrips = await ac.get("/api/v1/places/search?area_zone=day_trips&limit=100")
        assert resp_daytrips.status_code == 200
        d_daytrips = resp_daytrips.json()
        assert d_daytrips["total"] >= 5
        for p in d_daytrips["results"]:
            assert p["area_zone"] == "day_trips"
            # Ensure day trips include places like Mahabalipuram or Kanchipuram
            assert p["district"] in ["Chengalpattu", "Kanchipuram", "Tiruvallur"]

@pytest.mark.asyncio
async def test_places_discovery_keyword_search():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/places/search?query=Kapaleeshwarar")
        assert resp.status_code == 200
        d = resp.json()
        assert d["total"] >= 1
        assert "Kapaleeshwarar" in d["results"][0]["name"]

@pytest.mark.asyncio
async def test_places_discovery_detail_and_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Known item
        resp = await ac.get("/api/v1/places/chn_beach_marina")
        assert resp.status_code == 200
        p = resp.json()
        assert p["name"] == "Marina Beach & Promenade"
        assert p["lat"] == 13.0500
        assert p["ticket_price_inr"] == 0

        # Nonexistent item
        resp_404 = await ac.get("/api/v1/places/nonexistent_place_xyz")
        assert resp_404.status_code == 404

def test_planner_agent_has_full_chennai_catalog():
    chennai_places = DESTINATION_CATALOG["chennai"]["places"]
    assert len(chennai_places) >= 50
    # Confirm variety of categories available for trip planning
    cats = {p["category"] for p in chennai_places}
    assert "Beaches & Waterfronts" in cats or "Nature" in cats or "Culture" in cats
