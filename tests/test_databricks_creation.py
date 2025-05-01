import os
from typing import Optional, bool
from azure.identity import DefaultAzureCredential
from azure.mgmt.databricks import DatabricksManagementClient
from azure.mgmt.databricks.models import Workspace

# Environment variables for configuration
resource_group_name = os.environ.get("RESOURCE_GROUP_NAME")
workspace_name = os.environ.get("DATABRICKS_WORKSPACE_NAME")
expected_sku = "Standard"  # Or "Premium", depending on your deployment

def test_databricks_workspace_exists_and_has_correct_sku() -> bool:
    credential = DefaultAzureCredential()
    databricks_client = DatabricksManagementClient(
        credential, 
        str(os.environ.get("SUBSCRIPTION_ID"))
    )

    try:
        workspace = databricks_client.workspaces.get(resource_group_name, workspace_name)
        assert workspace is not None, f"Databricks workspace '{workspace_name}' not found in resource group '{resource_group_name}'."
        assert workspace.sku.name == expected_sku, f"Workspace SKU is '{workspace.sku.name}', expected '{expected_sku}'."
        print(f"Databricks workspace '{workspace_name}' exists and has SKU: {workspace.sku.name}")
        return True
    except Exception as e:
        print(f"Error checking workspace: {e}")
        return False

def test_databricks_workspace_properties():
    credential = DefaultAzureCredential()
    databricks_client = DatabricksManagementClient(credential, os.environ.get("SUBSCRIPTION_ID"))
    
    try:
        workspace = databricks_client.workspaces.get(resource_group_name, workspace_name)
        
        # Check essential properties
        assert workspace.provisioning_state == "Succeeded", f"Workspace provisioning state is {workspace.provisioning_state}"
        assert workspace.location is not None, "Workspace location is not set"
        assert workspace.managed_resource_group_id is not None, "Managed resource group ID is not set"
        
        print(f"Workspace properties verified successfully:")
        print(f"- Location: {workspace.location}")
        print(f"- Provisioning State: {workspace.provisioning_state}")
        print(f"- SKU: {workspace.sku.name}")
        return True
    except Exception as e:
        print(f"Error verifying workspace properties: {e}")
        return False

if __name__ == "__main__":
    # Ensure environment variables are set in your CI pipeline
    if not all([resource_group_name, workspace_name, os.environ.get("SUBSCRIPTION_ID")]):
        print("Error: Please set RESOURCE_GROUP_NAME, DATABRICKS_WORKSPACE_NAME, and SUBSCRIPTION_ID environment variables.")
    else:
        if test_databricks_workspace_exists_and_has_correct_sku():
            print("Databricks workspace verification passed.")
        else:
            print("Databricks workspace verification failed.")
            exit(1) # Exit with a non-zero code to indicate failure in the pipeline