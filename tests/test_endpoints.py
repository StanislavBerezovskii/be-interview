import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import Generator
from unittest.mock import patch
from uuid import uuid4
from fastapi import status
import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.core.db import get_database_session
from app.main import app
from app.models import Location, Organisation

_ALEMBIC_INI_PATH = Path(__file__).parent.parent / "alembic.ini"


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def apply_alembic_migrations() -> Generator[None, None, None]:
    # Creates test database per test function
    test_db_file_name = f"test_{uuid4()}.db"
    database_path = Path(test_db_file_name)
    try:
        test_db_url = f"sqlite:///{test_db_file_name}"
        alembic_cfg = alembic.config.Config(_ALEMBIC_INI_PATH)
        alembic_cfg.attributes["sqlalchemy_url"] = test_db_url
        alembic.command.upgrade(alembic_cfg, "head")
        test_engine = create_engine(test_db_url, echo=True)
        with patch("app.db.get_engine") as mock_engine:
            mock_engine.return_value = test_engine
            yield
    finally:
        database_path.unlink(missing_ok=True)


def test_endpoints(test_client: TestClient) -> None:
    list_of_organisation_names_to_create = ["organisation_a", "organisation_b", "organisation_c"]

    # Validate that organisations do not exist in database
    with get_database_session() as database_session:
        organisations_before = database_session.query(Organisation).all()
        database_session.expunge_all()
    assert len(organisations_before) == 0

    # Create organisations
    for organisation_name in list_of_organisation_names_to_create:
        response = test_client.post("/api/organisations/", json={"name": organisation_name})
        print(f"STATUS CODE: {response.status_code}")
        assert response.status_code == status.HTTP_200_OK

    # Validate that organisations exist in database
    with get_database_session() as database_session:
        organisations_after = database_session.query(Organisation).all()
        database_session.expunge_all()
    created_organisation_names = set(organisation.name for organisation in organisations_after)
    assert created_organisation_names == set(list_of_organisation_names_to_create)

    # Validate that created organisations can be retried via API
    response = test_client.get("/api/organisations")
    organisations = set(organisation["name"] for organisation in response.json())
    assert set(organisations) == created_organisation_names

    list_of_location_data_to_create = [
        {"location_name": "location_a", "longitude": 0.0, "latitude": 0.0},
        {"location_name": "location_b", "longitude": 0.0, "latitude": 0.0},
        {"location_name": "location_c", "longitude": 0.0, "latitude": 0.0},
    ]

    # Create locations for each organisation with unique names
    for idx, organisation in enumerate(organisations_after):
        for loc_idx, location_data in enumerate(list_of_location_data_to_create):
            unique_location_data = location_data.copy()
            unique_location_data["location_name"] = f"{location_data['location_name']}_{idx + 1}_{loc_idx + 1}"
            response = test_client.post(
                f"/api/organisations/{organisation.id}/locations",
                json=unique_location_data
            )
            assert response.status_code == status.HTTP_200_OK

    # Validate that locations exist in database
    with get_database_session() as database_session:
        locations_after = database_session.query(Location).all()
        database_session.expunge_all()
    assert len(locations_after) == 9

    # Validate that created locations can be retried via API
    for organisation in organisations_after:
        response = test_client.get(f"/api/organisations/{organisation.id}/locations")
        assert response.status_code == status.HTTP_200_OK
        locations = response.json()
        assert len(locations) == 3


if __name__ == "__main__":
    test_client = TestClient(app)
    test_endpoints(test_client)
