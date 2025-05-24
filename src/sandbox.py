import subprocess
import tempfile
import os
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
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

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
            safe_env = {"PYTHONUNBUFFERED": "1"}
            if env:
                safe_env.update(env)
            proc = subprocess.run(
                ["python3", tmp_path],
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