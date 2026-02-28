
from Backend.utils import llm
from Backend import routes
import subprocess

PATH_TO_ROUTES = "Backend/"
# Start the FastAPI server
subprocess.run(["python", "-m", "fastapi", "dev", f"{PATH_TO_ROUTES}routes.py"], shell=True, check=True)