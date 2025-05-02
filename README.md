# Azure Pipeline for Databricks Unit Tests and Deployment

This tutorial guides you through setting up an Azure Pipeline to run Databricks unit tests and automatically triggering a deployment to production if the tests are successful.

## Table of Contents

1. [Step 1: Create Your Unit Test File](#step-1-create-your-unit-test-file)
1. [Step 2: Create Azure Pipeline Configuration File](#step-2-create-azure-pipeline-configuration-file)
   - [Explanation](#explanation)
1. [Step 3: Set Up Azure DevOps Project](#step-3-set-up-azure-devops-project)
1. [Step 4: Verify and Deploy](#step-4-verify-and-deploy)

## Step 1: Create Your Unit Test

Example code included in [tests/](tests/)
Tests included: 

- python_Syntax_test.py 
  - Pass in a databricks notebook file and this will check the syntax of a databricks notebook
- security_egress_firewall_test.py
  - This will check if the IP of your databricks workspace is public facing
- sql_syntax_test.py
  - A simple syntax test, pass in SQL to check syntax 
- test_databricks_creation.py
  - Verify the successful creation and properties of the Databricks workspace. 
  - Set environment variables (RESOURCE_GROUP_NAME, DATABRICKS_WORKSPACE_NAME, SUBSCRIPTION_ID) in your Azure Pipeline configuration

## Step 2: Create Azure Pipeline Configuration File

Create an `azure-pipelines.yml` file in the root of your repository. This file will define the steps to set up the environment, run the tests, and trigger the production deployment.

```
trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x'
  displayName: 'Use Python 3.x'

- task: PipToolInstaller@0
  inputs:
    versionSpec: 'latest'
  displayName: 'Install Pip'

- task: Pip@0
  inputs:
    pipPackage: '-r requirements.txt'
  displayName: 'Install Python Dependencies'

- task: PythonTestRunner@0
  inputs:
    testWorkingDirectory: 'tests/' 
    pytestArgs: ''
    resultsFile: 'test-results.xml'
  displayName: 'Run Pytest Integration Tests'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'pytest'
    testResultsFiles: 'test-results.xml'
    publishRunAttachments: true
  condition: succeededOrFailed()
  displayName: 'Publish Test Results'
```
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
