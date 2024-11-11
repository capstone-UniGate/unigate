# Setup
1. Install `uv` (dependency manager): https://docs.astral.sh/uv/getting-started/installation/
2. The project is in python 3.12 and if you have another version `uv` will automatically install the required one. If it fails you can manually install it with: https://docs.astral.sh/uv/guides/install-python/
3. From now you **MUST must be inside the backend folder**
4. Install dependencies: `uv sync`
5. Activate the virtual environment: `source ./venv/bin/activate`
6. Select the python interpreter in your IDE: `.venv/bin/python`
7. Install pre-commit hooks: `pre-commit install`

# Development
1. Every time you work on the backend you need to enable the environment: `source ./venv/bin/activate`
2. From the backend folder start the backend with: `fastapi dev unigate/main.py`
