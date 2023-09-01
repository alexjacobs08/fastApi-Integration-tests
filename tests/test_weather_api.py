import pytest
from unittest.mock import patch
from unittest.mock import Mock
import os, sys
os.path.join(os.path.dirname(__file__), '../')
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import app.main


def test_get_weather(client):
    with patch('app.main.fetch_weather', return_value='sunny') as mock_fetch_weather:
        response = client.get("/weather/atlanta")
        assert response.status_code == 200
        assert response.json() == {'city': 'atlanta', 'weather': 'sunny'}
        mock_fetch_weather.assert_called_once_with('atlanta')


@pytest.fixture
def mock_fetch_weather_factory():
    def mock_fetch_weather(city):
        return "rainy"

    mock = Mock(side_effect=mock_fetch_weather)
    with patch.object(app.main, 'fetch_weather', new=mock):
        yield


def test_get_weather1(client, mock_fetch_weather_factory):
    response = client.get("/weather/atlanta")
    assert response.status_code == 200
    assert response.json() == {'city': 'atlanta', 'weather': 'rainy'}


@pytest.fixture
def mock_fetch_weather_parametrized(request):
    def mock_fetch_weather_factory(weather):
        def mock_fetch_weather(*args, **kwargs):
            return weather
        return mock_fetch_weather

    mock_weather = request.param
    with patch.object(app.main, 'fetch_weather', new=mock_fetch_weather_factory(mock_weather)):
        yield


@pytest.mark.parametrize('mock_fetch_weather_parametrized', ['cloudy'], indirect=True)
def test_get_weather_parameterized(client, mock_fetch_weather_parametrized):
    response = client.get("/weather/atlanta")
    assert response.status_code == 200
    assert response.json() == {'city': 'atlanta', 'weather': 'cloudy'}


