import unittest
from src.sandbox import Sandbox, SandboxResult

class TestSandbox(unittest.TestCase):
    def setUp(self):
        self.sandbox = Sandbox(timeout=1)

    def test_run_python_code_success(self):
        code = 'print("hello world")'
        result = self.sandbox.run_python_code(code)
        self.assertIsInstance(result, SandboxResult)
        self.assertEqual(result.stdout.strip(), "hello world")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.error, None)

    def test_run_python_code_error(self):
        code = 'raise ValueError("fail")'
        result = self.sandbox.run_python_code(code)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError", result.stderr)

    def test_run_python_code_timeout(self):
        code = 'import time\ntime.sleep(2)'
        result = self.sandbox.run_python_code(code)
        self.assertEqual(result.error, "timeout")

    def test_run_python_code_env(self):
        code = 'import os\nprint(os.environ.get("MYVAR"))'
        result = self.sandbox.run_python_code(code, env={"MYVAR": "testval"})
        self.assertEqual(result.stdout.strip(), "testval")

if __name__ == "__main__":
    unittest.main() 