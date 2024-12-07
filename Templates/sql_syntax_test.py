import unittest

class TestSQLSyntax(unittest.TestCase):
    def test_sql_syntax(self):
        # Replace the SQL string with the actual SQL query you want to test
        sql_query = """
        SELECT * FROM your_table
        """
        try:
            spark.sql(sql_query)
        except Exception as e:
            self.fail(f"SQL syntax error in query: {e}")

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        if result.wasSuccessful():
            print("\nAll tests passed successfully!")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())