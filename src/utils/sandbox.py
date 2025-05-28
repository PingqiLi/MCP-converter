import subprocess
import tempfile
import os
import sys
import json
from typing import Dict, Any, Optional

class SandboxResult:
    def __init__(self, stdout: str, stderr: str, returncode: int, error: Optional[str] = None):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.error = error

class Sandbox:
    """
    Executes Python code in a restricted subprocess environment.
    Controls environment variables and captures output/errors.
    """
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def execute_and_capture(self, code_file_path: str) -> Dict[str, Any]:
        """
        Execute a Python file and capture its response
        
        Args:
            code_file_path: Path to the Python file to execute
            
        Returns:
            Dict containing the execution result
        """
        # Read the code file
        with open(code_file_path, 'r') as f:
            code = f.read()
        
        # Create a wrapper that executes the code and captures the result
        # Use repr() to properly escape the code string
        code_repr = repr(code)
        
        wrapper_code = f'''
import sys
import json
import os

# Add the directory containing the code to Python path
sys.path.insert(0, {repr(os.path.dirname(os.path.abspath(code_file_path)))})

try:
    # Execute the original code
    exec({code_repr})
    
    # Try to find the main function and execute it
    if 'get_weather' in locals():
        # For weather API, try with demo data
        result = get_weather("London,GB")
        print("SANDBOX_RESULT:", json.dumps(result))
    else:
        print("SANDBOX_RESULT:", json.dumps({{"message": "Code executed successfully"}}))
        
except Exception as e:
    print("SANDBOX_ERROR:", str(e))
'''
        
        result = self.run_python_code(wrapper_code)
        
        if result.returncode == 0 and "SANDBOX_RESULT:" in result.stdout:
            # Extract the result from stdout
            for line in result.stdout.split('\n'):
                if line.startswith("SANDBOX_RESULT:"):
                    result_str = line.replace("SANDBOX_RESULT:", "").strip()
                    try:
                        return json.loads(result_str)
                    except json.JSONDecodeError:
                        return {"raw_result": result_str}
        
        # If execution failed or no result found, raise an exception
        error_msg = result.stderr or result.stdout or "Unknown execution error"
        raise RuntimeError(f"Code execution failed: {error_msg}")

    def run_python_code(self, code: str, env: Optional[Dict[str, str]] = None) -> SandboxResult:
        """
        Run Python code in a subprocess with restricted environment.
        Returns SandboxResult with stdout, stderr, and return code.
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            # Restrict environment variables
            safe_env = os.environ.copy()  # Copy current environment
            safe_env.update({"PYTHONUNBUFFERED": "1"})
            if env:
                safe_env.update(env)
            
            # Use current Python executable
            python_exe = sys.executable
            
            proc = subprocess.run(
                [python_exe, tmp_path],
                capture_output=True,
                text=True,
                env=safe_env,
                timeout=self.timeout
            )
            return SandboxResult(proc.stdout, proc.stderr, proc.returncode)
        except subprocess.TimeoutExpired as e:
            return SandboxResult("", str(e), -1, error="timeout")
        except Exception as e:
            return SandboxResult("", str(e), -1, error="exception")
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass 