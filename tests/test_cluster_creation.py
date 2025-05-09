import os
import pytest
import requests

DATABRICKS_INSTANCE = os.getenv("DATABRICKS_INSTANCE")  # e.g., 'https://<region>.azuredatabricks.net'
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
CLUSTER_ID = os.getenv("CLUSTER_ID")

HEADERS = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}"
}

@pytest.fixture(scope="module")
def databricks_url():
    return f"{DATABRICKS_INSTANCE}/api/2.0/clusters/get?cluster_id={CLUSTER_ID}"

def test_cluster_exists(databricks_url):
    response = requests.get(databricks_url, headers=HEADERS)
    assert response.status_code == 200, f"Cluster not found or request failed: {response.text}"
    data = response.json()
    assert data.get("state") in ["RUNNING", "TERMINATED"], f"Unexpected cluster state: {data.get('state')}"

if __name__ == "__main__":
    pytest.main(["-v", "--disable-warnings"])
