import argparse
import os
import sys

#Requests bruges til at lave HTTP kald til et api
import requests
from dotenv import load_dotenv

#Funktion som returnerer en api nøgle som en streng
def read_api_key(cli_key: str | None) -> str:
    # Hvis --key er givet bruges strip fjerner mellemrum før og efter
    if cli_key and cli_key.strip():
        return cli_key.strip()

    # Ellers læs fra .env hvis ikke givet i terminalen
    load_dotenv()
    #Os henter værdien fra miljøvariablen 
    env_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    #Hvis ikke findes, returner fejl.
    print(
        "Fejl: Ingen API key fundet.\n"
        "Brug enten: python valuta.py --key DIN_NOEGLE 100 DKK EUR\n"
        "Eller lav en .env fil med: EXCHANGE_RATE_API_KEY=DIN_NOEGLE",
        file=sys.stderr,
    )
    sys.exit(1)

# Funktion som henter kursen fra api
# Funktionen returnerer en float med kursen
def fetch_rate(api_key: str, from_currency: str, to_currency: str) -> float:
    # Bruger f string, så jeg kan indsætte variabler.
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    resp = requests.get(url, timeout=15)
    data = resp.json()

    # Hvis ikke status kode er 200, returneres fejl
    if resp.status_code != 200 or data.get("result") != "success":
        error_type = data.get("error-type", "unknown_error")
        raise RuntimeError(f"API fejl: {error_type}")

    rate = data.get("conversion_rate")
    if not isinstance(rate, (int, float)):
        raise RuntimeError("API fejl: conversion_rate mangler/er ugyldig")

    return float(rate)

# Main funktion som er none, hvilket betyder den ikke returnerer nogen værdi
def main() -> None:

    # Den tekst som skrives i terminalen bliver parset python .\valuta.py 100 DKK EUR
    parser = argparse.ArgumentParser(description="Valutaomregner (ExchangeRate-API)")
    parser.add_argument("--key", help="API key til ExchangeRate-API (ellers læses fra .env)")
    parser.add_argument("amount", type=float, help="Beløb, fx 100")
    parser.add_argument("from_currency", help="Fra valuta, fx DKK")
    parser.add_argument("to_currency", help="Til valuta, fx EUR")

    #Læs det som skrives i terminalen og gem i args
    args = parser.parse_args()

    api_key = read_api_key(args.key)
    from_cur = args.from_currency.upper()
    to_cur = args.to_currency.upper()

    #Prøv med den modtaget værdi, at returnere et svar
    try:
        rate = fetch_rate(api_key, from_cur, to_cur)
        #Den matematiske udregning
        converted = args.amount * rate
        print(f"{args.amount:.2f} {from_cur} = {converted:.2f} {to_cur} (kurs {rate})")
    except Exception as e:
        print(f"Fejl: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()