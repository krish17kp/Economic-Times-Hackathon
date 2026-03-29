"""
API integration tests for waste endpoints.
Location: backend/tests/test_api_waste.py
"""


class TestWasteTypes:
    def test_get_waste_types_no_auth(self, client):
        response = client.get("/api/v1/waste/types")
        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert len(data["types"]) == 5

    def test_waste_type_has_hindi_label(self, client):
        response = client.get("/api/v1/waste/types")
        types = response.json()["types"]
        rice = next(t for t in types if t["id"] == "rice_straw")
        assert rice["label_hi"] == "धान का पुआल"
