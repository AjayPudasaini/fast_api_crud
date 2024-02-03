## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AjayPudasaini/fast_api_crud
    ```

2. **Setup environment:**

    ```bash
    cd fast_api_crud
    ```

3. **Activate environment:**

    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS and Linux
    source venv/bin/activate
    ```

4. **Install requirements:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Change PostgreSQL URL:**

    Update the PostgreSQL URL in `src/database/database.py` to match your database configuration.

6. **Run the local server:**

    ```bash
    uvicorn main:app --reload
    ```

## Usage

After starting the server, you can access the API documentation in your browser at `localhost:8000/docs/`. The Swagger UI will allow you to interact with the API endpoints.


