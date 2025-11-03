<div align="center">

# Virtual Businessman - Financial Insights Application

A console-based Python application that provides historical financial insights using LangGraph. The application fetches exchange rates and gold prices for any given date.

</div>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [API Sources](#api-sources)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Environment Setup](#environment-setup)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Author](#author)

## Overview

This application acts as a virtual businessman, providing financial insights by:

- Fetching historical exchange rates for major currencies (USD to EUR, GBP, JPY)
- Retrieving historical gold prices per ounce
- Displaying the data in a clean, formatted console output

The application is built using **LangGraph** to structure the workflow as a state machine, enabling parallel data fetching for optimal performance.

## Features

- **Date-based queries**: Enter any date in YYYY-MM-DD format to get historical financial data
- **Parallel data fetching**: Exchange rates and gold prices are fetched simultaneously using LangGraph's parallel execution
- **Automatic fallbacks**: If data for the exact date isn't available, the application attempts to fetch the nearest available date
- **Multiple API sources**: Uses multiple free API endpoints with automatic fallback mechanisms
- **Simple console interface**: Clean, readable output format

## Requirements

- Python 3.10 or higher
- Internet connection (for API calls)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application from the command line:

```bash
python main.py
```

When prompted, enter a date in `YYYY-MM-DD` format (e.g., `2024-01-15`).

The application will:
1. Prompt you for a date
2. Fetch exchange rates and gold prices in parallel
3. Display a formatted report with all the financial data

## Project Structure

```
search-agent/
├── main.py              # Main application file with LangGraph workflow
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── ENV_SETUP.md          # Environment setup guide
├── src/                  # Source code directory (for future modularization)
│   └── README.md
├── tests/                # Test files directory
│   └── README.md
├── docs/                 # Documentation directory
│   └── README.md
├── data/                 # Data storage directory
│   └── README.md
└── logs/                 # Application logs directory
    └── README.md
```

## How It Works

The application uses LangGraph to define a state machine workflow:

1. **get_date**: Prompts the user for a date input
2. **fetch_exchange**: Fetches exchange rates from free APIs (parallel)
3. **fetch_gold**: Fetches gold prices from free APIs (parallel)
4. **compile**: Compiles all fetched data into a formatted report
5. **display**: Displays the final results

The exchange rate and gold price fetching nodes run in parallel, improving performance.

## API Sources

- **Exchange Rates**: 
  - Primary: `fawazahmed0/currency-api` via jsDelivr CDN (completely free, open source, no authentication required)
  - Fallback: GitHub raw endpoint (same API, alternative source)

- **Gold Prices**:
  - Primary: `fawazahmed0/currency-api` for XAU (Gold) via jsDelivr CDN (completely free, open source, no authentication required)
  - Automatic fallback to nearest available date if exact date not found
  - Uses XAU currency code to get gold price per ounce in USD

## Error Handling

The application includes basic error handling:
- Invalid date formats default to today's date
- Failed API calls show warnings and return "N/A" values
- Automatic fallback to alternative APIs if primary sources fail

## Configuration

The application can be configured using environment variables. Copy `.env.example` to `.env` and modify as needed:

```bash
# Linux/Mac
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Currently, the application uses free APIs that don't require API keys. If you switch to APIs that require authentication, add your keys to the `.env` file.

Available configuration options:
- `API_TIMEOUT`: Timeout for API requests (default: 10 seconds)
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)

For detailed environment setup instructions, see [ENV_SETUP.md](ENV_SETUP.md).

## Environment Setup

See [ENV_SETUP.md](ENV_SETUP.md) for complete instructions on setting up environment variables.

## Limitations

- Free API tiers may have rate limits
- Historical data availability depends on the API sources
- Some dates (especially weekends/holidays) may not have market data available

## Future Enhancements

Potential improvements could include:
- Social media sentiment analysis (Twitter/X integration)
- Additional financial instruments (stocks, cryptocurrencies)
- Data caching for frequently requested dates
- Export functionality (CSV, JSON)

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Author

Created as a demonstration of LangGraph for building stateful financial applications.

