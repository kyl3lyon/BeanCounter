from api.woocommerce import get_wc_api


# Test the get_wc_api function
def test_connection():
    wc_api = get_wc_api()
    response = wc_api.get("products")
    assert response.status_code == 200
    print("Connection test passed. Response status code:", response.status_code)

if __name__ == "__main__":
    test_connection()