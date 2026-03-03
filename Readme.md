# Valuta CLI

CLI tool til valutaomregning med ExchangeRate-API.

## Setup (Windows PowerShell)

1) Clone repo:
git clone <REPO_URL>
cd Valuta-CLI

2) Opret virtual environment:
python -m venv .venv

3) Aktivér:
.\.venv\Scripts\Activate.ps1

4) Installér dependencies:
pip install -r requirements.txt

## Brug

### Med key i kommandoen
python valuta.py --key DIN_NOEGLE 100 DKK EUR

### Med .env fil (anbefalet)
Lav en fil `.env` i projektmappen:
EXCHANGE_RATE_API_KEY=DIN_NOEGLE

Kør:
python valuta.py 100 DKK EUR
