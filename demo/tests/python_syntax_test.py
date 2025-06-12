import unittest

class TestPythonSyntax(unittest.TestCase):
    def test_syntax(self):
        try:
            with open('/dbfs/FileStore/daily_report.py', 'r') as file:  # Adjust the path as needed
                code = file.read()
            compile(code, 'daily_report.py', 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in file: {e}")

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        if result.wasSuccessful():
            print("\nAll tests passed successfully!")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner(verbosity=0))