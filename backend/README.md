# Setup
1. Install `uv` (dependency manager): https://docs.astral.sh/uv/getting-started/installation/
2. The project is in python 3.12 and if you have another version `uv` will automatically install the required one. If it fails you can manually install it with: https://docs.astral.sh/uv/guides/install-python/
3. From now you **MUST must be inside the backend folder**
4. Install dependencies: `uv sync`
5. Activate the virtual environment: `source .venv/bin/activate`
6. Select the python interpreter in your IDE: `.venv/bin/python`
7. Install pre-commit hooks: `pre-commit install`

# Development
1. Every time you work on the backend you need to enable the environment: `source ./venv/bin/activate`
2. From the backend folder start the backend with: `fastapi dev unigate/main.py`

## Folder Structure & Route Organization

- **Folder Structure for Routes**: Routes are organized in the `routes` directory based on HTTP methods and functionality. For example:
  - **GET routes**: Correspond to routes that retrieve data, like fetching details of resources. These routes are typically defined in directories like `routes/get/`.
  - **POST routes**: Correspond to routes that create or update resources. These routes can be placed in directories like `routes/post/`.

  This organization helps modularize the code and keeps each HTTP method well-organized for better maintainability.

## Configuration & Database Setup

1. **Environment Configuration**:
   - Create a `.env` file in the backend directory by following the provided example file.
   - Set `user=postgres` and `password=postgres` to ensure consistent authentication across environments.

2. **Database Initialization**:
   - To create the tables, initialize the database by running the script in `core/database.py`. This will set up the required schema for the application.

3. **Deploy PostgreSQL Using Docker Compose**:
   - Start a PostgreSQL instance using Docker Compose for a straightforward setup.
   - If port `5432` is already occupied on your system, change **only the first occurrence** of `5432` in the `docker-compose.yml` file to your preferred port (e.g., `5433:5432`).
   - Update your `.env` file to specify this custom port, if changed.
   - **IMPORTANT**: After testing, revert the `docker-compose.yml` port mapping to `5432:5432` before pushing changes, to maintain consistency for other users.
