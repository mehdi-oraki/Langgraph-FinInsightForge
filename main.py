"""
Virtual Businessman - Financial Insights Application
A simple console-based application using LangGraph to fetch historical
exchange rates and gold prices for a given date.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
import requests
from datetime import datetime


class FinancialState(TypedDict):
    """State structure for the financial insights graph."""
    date1: str
    date2: str
    exchange_rates1: dict
    exchange_rates2: dict
    gold_price1: dict
    gold_price2: dict
    location: dict
    weather: dict
    output: str


def get_user_date(state: FinancialState) -> dict:
    """Node: Prompt user for two date inputs."""
    print("\n" + "="*60)
    print("Virtual Businessman - Financial Insights")
    print("="*60)
    date1 = input("Enter start date (YYYY-MM-DD): ").strip()
    date2 = input("Enter end date   (YYYY-MM-DD): ").strip()
    
    # Validate date format
    try:
        datetime.strptime(date1, "%Y-%m-%d")
    except ValueError:
        print("Invalid start date. Using today's date.")
        date1 = datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date2, "%Y-%m-%d")
    except ValueError:
        print("Invalid end date. Using today's date.")
        date2 = datetime.now().strftime("%Y-%m-%d")
    return {"date1": date1, "date2": date2}


def _fetch_exchange_for_date(date: str) -> dict:
    
    # Using fawazahmed0/currency-api (completely free, open source, no auth required)
    try:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/usd.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usd_rates = data.get("usd", {})
            rates = {
                "EUR": usd_rates.get("eur", "N/A"),
                "GBP": usd_rates.get("gbp", "N/A"),
                "JPY": usd_rates.get("jpy", "N/A"),
            }
            return {"exchange_rates": rates}
        
        # Fallback: Try alternative endpoint format
        url_alt = f"https://raw.githubusercontent.com/fawazahmed0/currency-api/1/{date}/currencies/usd.json"
        response = requests.get(url_alt, timeout=10)
        if response.status_code == 200:
            data = response.json()
            usd_rates = data.get("usd", {})
            rates = {
                "EUR": usd_rates.get("eur", "N/A"),
                "GBP": usd_rates.get("gbp", "N/A"),
                "JPY": usd_rates.get("jpy", "N/A"),
            }
            return {"exchange_rates": rates}
    
    except Exception as e:
        print(f"Warning: Could not fetch exchange rates: {e}")
    
    # Default fallback
    return {"exchange_rates": {"EUR": "N/A", "GBP": "N/A", "JPY": "N/A"}}


def fetch_exchange_1(state: FinancialState) -> dict:
    """Node: Fetch exchange rates for date1."""
    date = state["date1"]
    res = _fetch_exchange_for_date(date)
    return {"exchange_rates1": res.get("exchange_rates", {})}


def fetch_exchange_2(state: FinancialState) -> dict:
    """Node: Fetch exchange rates for date2."""
    date = state["date2"]
    res = _fetch_exchange_for_date(date)
    return {"exchange_rates2": res.get("exchange_rates", {})}


def _fetch_gold_for_date(date: str) -> dict:
    
    try:
        # Using fawazahmed0/currency-api for gold (XAU - Gold ounce)
        # This API is completely free, open source, and requires no authentication
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/xau.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            xau_rates = data.get("xau", {})
            # XAU price in USD (gold per ounce)
            price = xau_rates.get("usd", "N/A")
            if price != "N/A":
                return {"gold_price": {"price_per_ounce": price, "currency": "USD"}}
        
        # Fallback: Try alternative GitHub raw endpoint
        url_alt = f"https://raw.githubusercontent.com/fawazahmed0/currency-api/1/{date}/currencies/xau.json"
        response = requests.get(url_alt, timeout=10)
        if response.status_code == 200:
            data = response.json()
            xau_rates = data.get("xau", {})
            price = xau_rates.get("usd", "N/A")
            if price != "N/A":
                return {"gold_price": {"price_per_ounce": price, "currency": "USD"}}
        
        # Fallback: Try previous day if exact date not available
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            prev_date = (date_obj.replace(day=1) if date_obj.day == 1 else date_obj.replace(day=date_obj.day-1)).strftime("%Y-%m-%d")
            url_prev = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{prev_date}/v1/currencies/xau.json"
            response = requests.get(url_prev, timeout=10)
            if response.status_code == 200:
                data = response.json()
                xau_rates = data.get("xau", {})
                price = xau_rates.get("usd", "N/A")
                if price != "N/A":
                    return {"gold_price": {"price_per_ounce": price, "currency": "USD", "note": "Nearest available date"}}
        except:
            pass
    
    except Exception as e:
        print(f"Warning: Could not fetch gold price: {e}")
    
    # Final fallback
    return {"gold_price": {"price_per_ounce": "N/A", "currency": "USD"}}


def fetch_gold_1(state: FinancialState) -> dict:
    """Node: Fetch gold price for date1."""
    date = state["date1"]
    res = _fetch_gold_for_date(date)
    return {"gold_price1": res.get("gold_price", {})}


def fetch_gold_2(state: FinancialState) -> dict:
    """Node: Fetch gold price for date2."""
    date = state["date2"]
    res = _fetch_gold_for_date(date)
    return {"gold_price2": res.get("gold_price", {})}


def fetch_location(state: FinancialState) -> dict:
    """Node: Detect user's approximate location via IP (no auth)."""
    try:
        # Free IP geolocation (no auth). Rate-limited but fine for simple CLI.
        resp = requests.get("http://ip-api.com/json/", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")
            lat = data.get("lat", None)
            lon = data.get("lon", None)
            return {"location": {"city": city, "country": country, "lat": lat, "lon": lon}}
    except Exception as e:
        print(f"Warning: Could not detect location: {e}")
    return {"location": {"city": "Unknown", "country": "Unknown", "lat": None, "lon": None}}


def fetch_weather(state: FinancialState) -> dict:
    """Node: Fetch live temperature using Open-Meteo with detected lat/lon."""
    loc = state.get("location", {})
    lat = loc.get("lat")
    lon = loc.get("lon")
    if lat is None or lon is None:
        return {"weather": {"temperature_c": "N/A"}}
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            current = data.get("current", {})
            temp_c = current.get("temperature_2m", "N/A")
            return {"weather": {"temperature_c": temp_c}}
    except Exception as e:
        print(f"Warning: Could not fetch weather: {e}")
    return {"weather": {"temperature_c": "N/A"}}


def compile_output(state: FinancialState) -> dict:
    """Node: Compile and format all fetched data into a readable output."""
    date1 = state["date1"]
    date2 = state["date2"]
    rates1 = state.get("exchange_rates1", {})
    rates2 = state.get("exchange_rates2", {})
    gold1 = state.get("gold_price1", {})
    gold2 = state.get("gold_price2", {})
    loc = state.get("location", {})
    weather = state.get("weather", {})
    
    def pct(old, new):
        try:
            if old in ("N/A", None) or new in ("N/A", None):
                return "N/A"
            old_v = float(old)
            new_v = float(new)
            if old_v == 0:
                return "N/A"
            return f"{((new_v - old_v) / old_v) * 100:.2f}%"
        except Exception:
            return "N/A"

    gold_note1 = f" ({gold1.get('note', '')})" if gold1.get('note') else ""
    gold_note2 = f" ({gold2.get('note', '')})" if gold2.get('note') else ""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    output = f"""
{'='*60}
FINANCIAL INSIGHTS REPORT
{'='*60}
Dates: {date1} → {date2}

LOCATION & WEATHER:
  City, Country: {loc.get('city', 'Unknown')}, {loc.get('country', 'Unknown')}
  Live Temperature: {weather.get('temperature_c', 'N/A')} °C
  Now: {now_str}

EXCHANGE RATES (USD Base):
  Date {date1}  | EUR: {rates1.get('EUR', 'N/A')}  GBP: {rates1.get('GBP', 'N/A')}  JPY: {rates1.get('JPY', 'N/A')}
  Date {date2}  | EUR: {rates2.get('EUR', 'N/A')}  GBP: {rates2.get('GBP', 'N/A')}  JPY: {rates2.get('JPY', 'N/A')}
  Change (%)   | EUR: {pct(rates1.get('EUR'), rates2.get('EUR'))}  GBP: {pct(rates1.get('GBP'), rates2.get('GBP'))}  JPY: {pct(rates1.get('JPY'), rates2.get('JPY'))}

GOLD PRICE (USD/oz):
  Date {date1}: ${gold1.get('price_per_ounce', 'N/A')} {gold1.get('currency', 'USD')}{gold_note1}
  Date {date2}: ${gold2.get('price_per_ounce', 'N/A')} {gold2.get('currency', 'USD')}{gold_note2}
  Change (%): {pct(gold1.get('price_per_ounce'), gold2.get('price_per_ounce'))}

{'='*60}
"""
    
    return {"output": output}


def display_results(state: FinancialState) -> dict:
    """Node: Display the compiled results to the console."""
    print(state.get("output", "No output available."))
    return {}


def build_graph():
    """Build and return the LangGraph state machine."""
    workflow = StateGraph(FinancialState)
    
    # Add nodes
    workflow.add_node("get_date", get_user_date)
    workflow.add_node("fetch_location", fetch_location)
    workflow.add_node("fetch_weather", fetch_weather)
    workflow.add_node("fetch_exchange_1", fetch_exchange_1)
    workflow.add_node("fetch_exchange_2", fetch_exchange_2)
    workflow.add_node("fetch_gold_1", fetch_gold_1)
    workflow.add_node("fetch_gold_2", fetch_gold_2)
    workflow.add_node("compile", compile_output)
    workflow.add_node("display", display_results)
    
    # Define the graph flow
    workflow.set_entry_point("get_date")
    
    # After getting date, get location -> weather; then fetch finance data
    workflow.add_edge("get_date", "fetch_location")
    workflow.add_edge("fetch_location", "fetch_weather")
    
    # After weather, fetch finance data sequentially for simplicity
    workflow.add_edge("fetch_weather", "fetch_exchange_1")
    workflow.add_edge("fetch_exchange_1", "fetch_exchange_2")
    workflow.add_edge("fetch_exchange_2", "fetch_gold_1")
    workflow.add_edge("fetch_gold_1", "fetch_gold_2")
    workflow.add_edge("fetch_gold_2", "compile")
    
    # Display results and end
    workflow.add_edge("compile", "display")
    workflow.add_edge("display", END)
    
    return workflow.compile()


def main():
    """Main entry point for the application."""
    graph = build_graph()
    
    # Initialize state
    initial_state = {
        "date": "",
        "exchange_rates": {},
        "gold_price": {},
        "output": ""
    }
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    print("\nThank you for using Virtual Businessman!")


if __name__ == "__main__":
    main()

