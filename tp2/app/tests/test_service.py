import requests

BASE_URL = "http://localhost:8000"


def test_predict():
    test_data = {
        "inputs": [
            [5.1, 3.5, 1.4, 0.2],  # setosa
            [7.0, 3.2, 4.7, 1.4],  # versicolor
            [6.3, 3.3, 6.0, 2.5],  # virginica
        ]
    }

    response = requests.post(f"{BASE_URL}/predict", json=test_data)

    assert response.status_code == 200
    assert response.json()["predictions"] == [0, 1, 2]


if __name__ == "__main__":
    test_predict()
