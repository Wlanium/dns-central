# DNS Central 🌐

Multi-Provider Domain & DNS Management Tool für die zentrale Verwaltung aller Domains.

## Features

- **Multi-Provider Support**: Netcup, Porkbun, IONOS (weitere geplant)
- **Server-Gruppierung**: Alle Domains nach IP/Server gruppiert anzeigen
- **Schnellsuche**: Domain oder IP eingeben, sofort finden
- **API-basiert**: Direkt von den Providern, keine DNS-Auflösung nötig
- **Dark Mode**: Augenfreundliches Interface

## Quick Start

### Lokal

```bash
# Repo klonen
git clone https://github.com/Wlanium/dns-central.git
cd dns-central

# Environment einrichten
cp .env.example .env
# .env mit deinen API Keys füllen

# Dependencies installieren
pip install -r requirements.txt

# Starten
python run.py
```

→ http://localhost:5000

### Docker

```bash
cp .env.example .env
# .env editieren

docker-compose up -d
```

→ http://localhost:5050

## Konfiguration

`.env` Datei mit API Credentials:

```env
# Netcup CCP API
NETCUP_CUSTOMER_ID=12345
NETCUP_API_KEY=your-api-key
NETCUP_API_PASSWORD=your-api-password

# Porkbun (coming soon)
# PORKBUN_API_KEY=
# PORKBUN_SECRET_KEY=

# IONOS (coming soon)
# IONOS_PUBLIC_PREFIX=
# IONOS_SECRET=
```

## API Endpoints

| Endpoint | Beschreibung |
|----------|--------------|
| `GET /api/domains` | Alle Domains mit DNS Records |
| `GET /api/servers` | Domains gruppiert nach IP |
| `GET /api/domains/by-ip/<ip>` | Domains für eine IP finden |
| `GET /api/health` | Provider Status |

## Provider APIs

### Netcup
- API Key generieren: [CCP → Stammdaten → API](https://ccp.netcup.net)
- Doku: https://ccp.netcup.net/run/webservice/servers/endpoint.php

### Porkbun (geplant)
- API Docs: https://porkbun.com/api/json/v3/documentation

### IONOS (geplant)
- API Docs: https://developer.hosting.ionos.de/docs/dns

## Roadmap

- [x] Netcup Integration
- [ ] Porkbun Integration
- [ ] IONOS Integration
- [ ] DNS Record Editing
- [ ] Vergleich Soll/Ist (Config vs. aktuelle Auflösung)
- [ ] Alerts bei Abweichungen
- [ ] Export (CSV, JSON)

## License

MIT
