# Azure Pipeline for Databricks Unit Tests and Deployment

This tutorial guides you through setting up an Azure Pipeline to run Databricks unit tests in a dev environment and automatically triggering a deployment to production if the tests are successful.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Create Your Unit Test File](#step-1-create-your-unit-test-file)
3. [Step 2: Create Azure Pipeline Configuration File](#step-2-create-azure-pipeline-configuration-file)
   - [Explanation](#explanation)
4. [Step 3: Set Up Azure DevOps Project](#step-3-set-up-azure-devops-project)
5. [Step 4: Verify and Deploy](#step-4-verify-and-deploy)

## Step 1: Create Your Unit Test File

Ensure you have your unit test file (`security_egress_firewall_test.py`) ready. Here is the code:

```
import unittest
import ipaddress
import requests

def is_public_ip(ip):
    """
    Check if the IP address is public-facing.
    """
    ip = ipaddress.ip_address(ip)
    return not (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local or ip.is_multicast)

def get_ip_address(workspace_url):
    """
    Get the public IP address of the Databricks workspace.
    """
    response = requests.get(workspace_url)
    ip = response.json().get('ip')
    return ip

class TestDatabricksWorkspaceIP(unittest.TestCase):
    def test_workspace_ip(self):
        workspace_url = 'https://ifconfig.me/all.json'  # Example URL to get IP address
        ip = get_ip_address(workspace_url)
        print(f"Databricks Workspace IP: {ip}")
        self.assertTrue(is_public_ip(ip), f"{ip} should be public")

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        if result.wasSuccessful():
            print("\nAll tests passed successfully!")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())```


## Step 2: Create Azure Pipeline Configuration File

Create an `azure-pipelines.yml` file in the root of your repository. This file will define the steps to set up the environment, run the tests, and trigger the production deployment.

```
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

jobs:
- job: TestAndDeploy
  displayName: 'Test and Deploy Job'
  steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'
      addToPath: true

  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install dependencies'

  - script: |
      python -m unittest discover -s . -p 'security_egress_firewall_test.py'
    displayName: 'Run unit tests'

  - task: AzureCLI@2
    displayName: 'Deploy to Production'
    inputs:
      azureSubscription: '<Your Azure Subscription>'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        echo "Deploying to production..."
        # Add your production deployment script here
    condition: succeeded()```

    ### Explanation

1. **Trigger**: Specifies the branch to trigger the pipeline (e.g., `main`).
2. **Pool**: Defines the virtual machine image to use (e.g., `ubuntu-latest`).
3. **Jobs**: Defines a job named `TestAndDeploy`.
4. **Steps**:
   - **UsePythonVersion**: Sets up the Python version.
   - **Install dependencies**: Installs the required dependencies from `requirements.txt`.
   - **Run unit tests**: Runs the unit tests using `unittest`.
   - **Deploy to Production**: Deploys to production if the tests are successful. Replace `<Your Azure Subscription>` with your actual Azure subscription ID and add your production deployment script.

   ## Step 3: Set Up Azure DevOps Project

1. **Create a new project**: Go to Azure DevOps and create a new project.
2. **Create a new pipeline**: Navigate to Pipelines > Create Pipeline.
3. **Connect to your repository**: Select your repository where the `azure-pipelines.yml` file is located.
4. **Run the pipeline**: Save and run the pipeline.

## Step 4: Verify and Deploy

1. **Verify the pipeline**: Ensure that the pipeline runs successfully and the tests pass.
2. **Automatic deployment**: If the tests pass, the pipeline will automatically trigger the production deployment.
