import pytest
from fastapi.testclient import TestClient

from main import app, startup


client = TestClient(app)
startup()


@pytest.fixture()
def reset():
    client.put('/api/reset')


def test_booking_a_car(reset):
    body = {
        "source": {
            "x": 3,
            "y": 1
        },
        "destination": {
            "x": 8,
            "y": 6
        }
    }

    resp = client.post('/api/book', json=body)

    assert resp.status_code == 200

    assert resp.json() == {'car_id': 1, 'total_time': 4 + 10}


def test_booking_no_available(reset):
    body = {
        "source": {
            "x": 1,
            "y": 0
        },
        "destination": {
            "x": 1,
            "y": 1
        }
    }

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 1, 'total_time': 2}

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 2, 'total_time': 2}

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 3, 'total_time': 2}

    # all cars are taken
    resp = client.post('/api/book', json=body)
    assert resp.json() == {"status": "failed", "message": "No free cars available right now, please wait..."}

    # wait for 3 units
    for _ in range(3):
        client.post('/api/tick')

    # all cars should be free again
    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 1, 'total_time': 2}


def test_reset(reset):
    body = {
        "source": {
            "x": 1,
            "y": 0
        },
        "destination": {
            "x": 1,
            "y": 1
        }
    }

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 1, 'total_time': 2}

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 2, 'total_time': 2}

    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 3, 'total_time': 2}

    resp = client.put('/api/reset')
    assert resp.json() == {'status': 'OK'}

    # all cars should be reset and available
    resp = client.post('/api/book', json=body)
    assert resp.json() == {'car_id': 1, 'total_time': 2}
