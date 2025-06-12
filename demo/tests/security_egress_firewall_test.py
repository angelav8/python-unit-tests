import unittest
import ipaddress
import requests
##needs requests library 
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
    unittest.main(testRunner=CustomTestRunner())