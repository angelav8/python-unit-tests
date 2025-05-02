import requests
import json
import os

def test_databricks_cluster_status(host, token, cluster_id, org_id, port):
    """
    Integration test to check the status of a Databricks cluster.

    Args:
        host (str): The Databricks workspace host (e.g., https://your-workspace.azuredatabricks.net).
        token (str): A Databricks personal access token.
        cluster_id (str): The ID of the Databricks cluster to check.
        org_id (str): The Databricks organization ID.
        port (str): The port number for the Databricks API (typically '443' for HTTPS).

    Returns:
        bool: True if the cluster is running, False otherwise.
    """
    api_version = "2.0"
    endpoint = f"https://{host}:{port}/api/{api_version}/clusters/get"
    headers = {"Authorization": f"Bearer {token}", "X-Databricks-Org-Id": org_id}
    params = {"cluster_id": cluster_id}

    try:
        response = requests.get(endpoint, headers=headers, params=params, verify=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        cluster_info = response.json()
        cluster_state = cluster_info.get("state")
        print(f"Cluster ID: {cluster_id}, Current State: {cluster_state}")
        return cluster_state == "RUNNING"
    except requests.exceptions.RequestException as e:
        print(f"Error checking cluster status for ID {cluster_id}: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for cluster ID {cluster_id}")
        return False
    except KeyError:
        print(f"Error: 'state' key not found in the response for cluster ID {cluster_id}")
        return False

if __name__ == "__main__":
    # These would typically come from your CI/CD pipeline variables or environment variables
    databricks_host = os.environ.get("DATABRICKS_HOST")
    databricks_token = os.environ.get("DATABRICKS_TOKEN")
    target_cluster_id = os.environ.get("DATABRICKS_CLUSTER_ID")
    databricks_org_id = os.environ.get("DATABRICKS_ORG_ID")
    databricks_port = os.environ.get("DATABRICKS_PORT", "443")

    if not all([databricks_host, databricks_token, target_cluster_id, databricks_org_id]):
        print("Error: Please set the DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_CLUSTER_ID, and DATABRICKS_ORG_ID environment variables.")
    else:
        if test_databricks_cluster_status(databricks_host, databricks_token, target_cluster_id, databricks_org_id, databricks_port):
            print(f"Integration test passed: Cluster '{target_cluster_id}' is running.")
        else:
            print(f"Integration test failed: Cluster '{target_cluster_id}' is not running.")
            exit(1) # Exit with a non-zero code to indicate failure in the pipeline