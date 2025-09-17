# Python REST API Application

A simple REST API built with FastAPI for processing vectors (lists of numbers).

## Features

- Health check endpoint (`/api/v1/ping`)
- Vector reversal endpoint (`/api/v1/revert_vector`)
- Configurable host and port through environment variables

## Configuration

The application can be configured using the following environment variables:

| Variable | Description          | Default Value |
|----------|----------------------|---------------|
| HOST     | Host to bind to      | 127.0.0.1     |
| PORT     | Port to listen on    | 8000          |

### Using Environment Variables

You can set these environment variables in several ways:

1. **Directly in the command line:**
   ```bash
   HOST=0.0.0.0 PORT=8080 python main.py
   ```

2. **Using a .env file:**
   Create a `.env` file in the project root with your configuration:
   ```
   HOST=0.0.0.0
   PORT=8080
   ```

3. **Exporting in your shell:**
   ```bash
   export HOST=0.0.0.0
   export PORT=8080
   python main.py
   ```

## API Endpoints

### Ping Endpoint
- **URL:** `/api/v1/ping`
- **Method:** GET
- **Description:** Health check endpoint
- **Response:** `{"message": "pong"}`

### Revert Vector Endpoint
- **URL:** `/api/v1/revert_vector`
- **Method:** POST
- **Description:** Reverses a list of numbers
- **Request Body:** `[1.0, 2.0, 3.0]`
- **Response:** `[3.0, 2.0, 1.0]`

## Running the Application

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. The application will start on `http://127.0.0.1:8000` by default.

## Testing

Run tests with pytest:
```bash
pip install pytest
pytest
