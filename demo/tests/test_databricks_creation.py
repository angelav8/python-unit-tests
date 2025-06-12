import requests
import json
import os

def test_databricks_cluster_status(host, token, cluster_id, org_id, port):
    """
    Integration test to check the status of a Databricks cluster.

    Args:
        host (str): The Databricks workspace host.
        token (str): A Databricks personal access token.
        cluster_id (str): The ID of the Databricks cluster to check.
        org_id (str): The Databricks organization ID.
        port (str): The port number for the Databricks API.

    Returns:
        bool: True if the cluster is running, False otherwise.
    """
    api_version = "2.0"
    endpoint = f"https://{host}:{port}/api/{api_version}/clusters/get"
    headers = {"Authorization": f"Bearer {token}", "X-Databricks-Org-Id": org_id}
    params = {"cluster_id": cluster_id}

    try:
        response = requests.get(endpoint, headers=headers, params=params, verify=True)
        response.raise_for_status()
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
    # Setting explicit values directly here:
    databricks_host = "your-databricks-host.azuredatabricks.net"
    databricks_token = "your-databricks-personal-access-token"
    target_cluster_id = "your-cluster-id"
    databricks_org_id = "your-databricks-org-id"
    databricks_port = "443"

    if test_databricks_cluster_status(databricks_host, databricks_token, target_cluster_id, databricks_org_id, databricks_port):
        print(f"Integration test passed: Cluster '{target_cluster_id}' is running.")
    else:
        print(f"Integration test failed: Cluster '{target_cluster_id}' is not running.")
        exit(1)