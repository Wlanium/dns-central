"""
DNS Central Routes
"""

import json
from flask import Blueprint, render_template, request, current_app, jsonify
from .providers import NetcupAPI

bp = Blueprint("main", __name__)


def get_netcup_client():
    """Create Netcup API client from config"""
    domains_str = current_app.config.get("NETCUP_DOMAINS", "")
    domains = [d.strip() for d in domains_str.split(",") if d.strip()] if domains_str else []

    return NetcupAPI(
        customer_id=current_app.config["NETCUP_CUSTOMER_ID"],
        api_key=current_app.config["NETCUP_API_KEY"],
        api_password=current_app.config["NETCUP_API_PASSWORD"],
        domains=domains
    )


@bp.route("/")
def index():
    """Dashboard - Übersicht aller Domains"""
    return render_template("index.html")


@bp.route("/api/domains")
def api_domains():
    """API: Liste aller Domains mit Records"""
    try:
        with get_netcup_client() as client:
            domains = client.list_domains()
            result = []
            
            for domain in domains:
                records = client.get_dns_records(domain)
                a_records = [r for r in records if r.get("type") == "A"]
                
                result.append({
                    "domain": domain,
                    "provider": "netcup",
                    "records": records,
                    "a_records": a_records,
                    "ips": list(set(r.get("destination") for r in a_records))
                })
            
            return jsonify({"status": "success", "domains": result})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/api/domains/by-ip/<ip>")
def api_domains_by_ip(ip):
    """API: Finde alle Domains die auf eine IP zeigen"""
    try:
        with get_netcup_client() as client:
            matches = client.find_domains_by_ip(ip)
            return jsonify({"status": "success", "ip": ip, "domains": matches})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/api/servers")
def api_servers():
    """API: Gruppiere Domains nach Server/IP"""
    try:
        # Load server info from config
        server_info = json.loads(current_app.config.get("SERVERS", "{}"))

        with get_netcup_client() as client:
            domains = client.list_domains()
            servers = {}

            for domain in domains:
                records = client.get_dns_records(domain)

                for record in records:
                    record_type = record.get("type")
                    if record_type in ("A", "AAAA"):
                        ip = record.get("destination")
                        hostname = record.get("hostname", "@")

                        if ip not in servers:
                            info = server_info.get(ip, {})
                            # Support both old format (string) and new format (dict)
                            if isinstance(info, str):
                                name = info
                                server_id = ""
                            else:
                                name = info.get("name", "")
                                server_id = info.get("id", "")
                            servers[ip] = {
                                "name": name,
                                "id": server_id,
                                "type": record_type,
                                "domains": []
                            }

                        fqdn = domain if hostname == "@" else f"{hostname}.{domain}"
                        servers[ip]["domains"].append({
                            "domain": domain,
                            "hostname": hostname,
                            "fqdn": fqdn
                        })

            return jsonify({"status": "success", "servers": servers})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/api/health")
def api_health():
    """API: Check provider connectivity"""
    results = {"netcup": False}
    
    try:
        with get_netcup_client() as client:
            results["netcup"] = True
    except:
        pass
    
    return jsonify(results)
