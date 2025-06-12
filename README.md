# Getting started with Integration tests for Databricks CI/CD

This tutorial guides you through setting up an Azure Pipeline which triggers integration tests in python for databricks. This setup can also be used for unit testing or integration testing any python project. 

## Table of Contents

1. [Step 1: Create Your Unit Test File](#step-1-create-your-unit-test-file)
1. [Step 2: Create Azure Pipeline Configuration File](#step-2-create-azure-pipeline-configuration-file)
1. [Step 3: Set Up Azure DevOps Project](#step-3-set-up-azure-devops-project)
1. [Step 4: Verify and Deploy](#step-4-verify-and-deploy)

## Step 1: Create Your Unit Test File

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

Create an Azure pipelines CI configuration file, within this file you should have the below tasks 

```
#Install python 
steps:
- task: UsePythonVersion@0
  displayName: 'Use Python 3.x'
  inputs:
      versionSpec: 3.x

# Install pytest and any other dependancies
- script: |
   pip install pytest
 displayName: 'Install pytest'


# The below block creates a folder for the logs to sit on 
# Runs pytests in a tests/ folder 
# Outputs the test results in a XML file using azures predefined variables
# the || true condition will pass to the next task even if the python tests fail
# We proceed to the next task even though the tests fail to publish the test results
- script: |
   mkdir -p $(Build.Repository.LocalPath)/logs
   python -m pytest tests/ --junitXML=$(Build.Repository.LocalPath)/logs/test-results.xml || true
  displayName: 'Run Pytest Integration Tests'


# This Azure pipelines task publishes the test results
# This allows you to visulise the reports and dashboards related to testing
# This task will fail if the tests fail 
- task: PublishTestResults@2
  inputs:
    testResultsFiles: 'test-*.xml'
    publishRunAttachments: true
    failTaskOnFailedTests: true
  displayName: 'Publish Test Results'
```

  
   ## Step 3: Set Up Azure DevOps Project

1. **Create a new project**: Go to Azure DevOps and create a new project.
2. **Import/Upload the demo project** Change variables to suit your own configuration 
3. **Create a new pipeline**: Navigate to Pipelines > Create Pipeline.
4. **Connect to your repository**: Select your repository where the `azure-pipelines.yml` file is located.
5. **Run the pipeline**: Save and run the pipeline.

## Step 4: Verify and Deploy

1. **Verify the pipeline**: Ensure that the pipeline runs successfully and the tests pass.
2. **Automatic deployment**: If the tests pass, the pipeline will automatically trigger the production deployment.
