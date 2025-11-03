# Environment Variables Setup

This guide explains how to set up environment variables for the Virtual Businessman application.

## Quick Setup

1. **Create `.env` file**:
   ```bash
   # On Linux/Mac
   cp .env.example .env
   
   # On Windows (PowerShell)
   Copy-Item .env.example .env
   ```

2. **Edit `.env` file** with your preferred text editor:
   ```bash
   # Linux/Mac
   nano .env
   
   # Windows
   notepad .env
   ```

3. **Configure your variables** (currently optional since the app uses free APIs):
   - Add API keys if you switch to APIs that require authentication
   - Adjust timeout settings if needed
   - Enable debug mode if developing

## Environment Variables

### API Configuration
- `EXCHANGE_RATE_API_KEY`: API key for exchange rate service (if required)
- `GOLD_PRICE_API_KEY`: API key for gold price service (if required)

### Application Settings
- `DEBUG`: Enable debug mode (`True`/`False`, default: `False`)
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, default: `INFO`)
- `API_TIMEOUT`: Timeout for API requests in seconds (default: `10`)
- `DATE_FORMAT`: Date format string (default: `YYYY-MM-DD`)

## Notes

- The `.env` file is already included in `.gitignore` and will not be committed to version control
- Currently, the application uses completely free APIs that don't require authentication
- You only need to configure `.env` if you plan to use APIs that require API keys

