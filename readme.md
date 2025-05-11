# Farming Simulator Server API

This project provides a FastAPI-based API to fetch and display information and game settings from a Farming Simulator dedicated server.

## Project Purpose

The primary goal of this project is to expose dedicated server statistics and game settings via a simple REST API. This allows other applications or services to easily consume this data.

## Features

*   Fetches general server information (name, map, player count, online players, mods).
*   Fetches current game settings and statistics (money, playtime).
*   Simple caching mechanism to reduce load on the source server (data refreshed every 59 seconds).

## Quick Start

Follow these steps to get the API server up and running:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Dragons-Dev/FS25-Api
    cd FS25-Api
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    pip install fastapi uvicorn requests
    ```
    (Consider creating a `requirements.txt` file for easier dependency management).

3.  **Run the application:**
    The API server uses Uvicorn.
    ```bash
    python app.py
    ```
    Alternatively, you can run it directly with Uvicorn for more options (e.g., auto-reload):
    ```bash
    uvicorn app:app --reload
    ```
    The API will be available at `http://localhost:8000`.

4.  **Access API Endpoints:**
    *   Health Check: `http://localhost:8000/health`
    *   Server Info: `http://localhost:8000/server_info`
    *   Game Settings: `http://localhost:8000/game_settings`

## Developer Guide

### Project Structure
 ├── app.py # Main FastAPI application, defines API endpoints \
 ├── FSParser # Module for fetching and parsing game data \
 ├── init.py # Makes FSParser a Python package \
 └── stats.py # Logic for HTTP requests and XML parsing \
 └── README.md # This file
 
### Key Components

*   **`app.py`**:
    *   Uses FastAPI to define the web application and its routes (`/health`, `/server_info`, `/game_settings`).
    *   Handles incoming requests and calls the appropriate functions from the `FSParser` module.
    *   Returns JSON responses.
*   **`FSParser/stats.py`**:
    *   `fetch_dedi_info()`: Fetches and parses `dedicated-server-stats.xml`. This includes server details, player information, and mods.
    *   `fetch_dedi_settings()`: Fetches and parses `dedicated-server-savegame.html` (specifically the careerSavegame data). This includes game settings and statistics like money and playtime.
    *   `_requester(url)`: A utility function to make HTTP GET requests. It includes a simple in-memory cache (`last_checked`) to avoid refetching data from the target server more than once every 59 seconds.
    *   `_utils_guess_type(value)`: A helper function to attempt to convert string values parsed from XML into appropriate Python types (int, float, bool, or string).

### How It Works

1.  When a request hits an endpoint in `app.py` (e.g., `/server_info`), the corresponding route handler function is executed.
2.  This function calls either `fetch_dedi_info()` or `fetch_dedi_settings()` from `FSParser.stats`.
3.  Inside `FSParser.stats`, the `_requester()` function is used to get the raw XML data from the specified Farming Simulator server feed URL.
    *   The `_requester` first checks its `last_checked` cache. If valid cached data exists (checked within the last 59 seconds), it returns the cached data.
    *   Otherwise, it makes a new HTTP GET request using the `requests` library.
4.  The XML data is then parsed using `xml.etree.ElementTree`.
5.  The parsed data is transformed into a Python dictionary with a structured format.
6.  The `_utils_guess_type` function is used to convert text values from the XML into more specific Python data types.
7.  The resulting dictionary is returned to `app.py`, which then sends it as a JSON response.

### Modifying or Extending

*   **Adding New Endpoints**:
    1.  Define a new path operation decorator (e.g., `@app.get("/new_endpoint")`) in `app.py`.
    2.  Create a corresponding function that might call new or existing logic in `FSParser`.
*   **Changing Data Fetching/Parsing**:
    1.  Modify the URLs or parsing logic within the `fetch_dedi_info()` or `fetch_dedi_settings()` functions in `FSParser/stats.py`.
    2.  If new data sources or XML structures are involved, you might need to adjust the `ET.fromstring()` and subsequent element traversal.
*   **Configuration**:
    *   The URLs for the dedicated server feeds are hardcoded in `FSParser/stats.py`. For more flexibility, consider moving these to environment variables or a configuration file.

### Dependencies

*   `fastapi`: For building the API.
*   `uvicorn`: ASGI server to run the FastAPI application.
*   `requests`: For making HTTP requests to the game server.

Ensure these are installed, preferably within a virtual environment. If you create a `requirements.txt` file, it would typically look like this:

```txt
fastapi
uvicorn
requests
```
