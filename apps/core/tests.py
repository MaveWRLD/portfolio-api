from unittest.mock import patch

import pytest
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle


@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.mark.django_db
@patch.object(AnonRateThrottle, "THROTTLE_RATES", {"anon": "2/min", "user": "2/min"})
def test_anon_requests_are_throttled_past_configured_rate(client):
    for _ in range(2):
        response = client.get("/api/case-studies/")
        assert response.status_code == 200

    response = client.get("/api/case-studies/")
    assert response.status_code == 429
