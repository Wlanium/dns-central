"""
Netcup CCP API Provider
JSON-RPC based API for domain and DNS management
"""

import requests
from typing import Optional


class NetcupAPI:
    """Netcup CCP API Client"""
    
    API_URL = "https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON"
    
    def __init__(self, customer_id: str, api_key: str, api_password: str):
        self.customer_id = customer_id
        self.api_key = api_key
        self.api_password = api_password
        self.session_id: Optional[str] = None
    
    def _call(self, action: str, params: dict = None) -> dict:
        """Make JSON-RPC call to Netcup API"""
        payload = {
            "action": action,
            "param": {
                "customernumber": self.customer_id,
                "apikey": self.api_key,
                "apisessionid": self.session_id or "",
                **(params or {})
            }
        }
        
        response = requests.post(
            self.API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self) -> bool:
        """Authenticate and get session ID"""
        result = self._call("login", {
            "apipassword": self.api_password
        })
        
        if result.get("status") == "success":
            self.session_id = result.get("responsedata", {}).get("apisessionid")
            return True
        return False
    
    def logout(self) -> bool:
        """End session"""
        if not self.session_id:
            return True
            
        result = self._call("logout")
        if result.get("status") == "success":
            self.session_id = None
            return True
        return False
    
    def list_domains(self) -> list:
        """Get all domains for this account"""
        if not self.session_id:
            self.login()
        
        result = self._call("listallDomains")
        
        if result.get("status") == "success":
            domains = result.get("responsedata", [])
            # Kann Liste von Strings oder Dicts sein
            if domains and isinstance(domains[0], dict):
                return [d.get("domainname") for d in domains]
            return domains if domains else []
        return []
    
    def get_dns_records(self, domain: str) -> list:
        """Get all DNS records for a domain"""
        if not self.session_id:
            self.login()
        
        result = self._call("infoDnsRecords", {
            "domainname": domain
        })
        
        if result.get("status") == "success":
            records = result.get("responsedata", {}).get("dnsrecords", [])
            return records if records else []
        return []
    
    def get_dns_zone(self, domain: str) -> dict:
        """Get DNS zone info for a domain"""
        if not self.session_id:
            self.login()
        
        result = self._call("infoDnsZone", {
            "domainname": domain
        })
        
        if result.get("status") == "success":
            return result.get("responsedata", {})
        return {}
    
    def get_all_domains_with_records(self) -> dict:
        """Convenience method: Get all domains with their DNS records"""
        domains = self.list_domains()
        result = {}
        
        for domain in domains:
            result[domain] = {
                "zone": self.get_dns_zone(domain),
                "records": self.get_dns_records(domain)
            }
        
        return result
    
    def find_domains_by_ip(self, target_ip: str) -> list:
        """Find all domains pointing to a specific IP"""
        all_data = self.get_all_domains_with_records()
        matching = []
        
        for domain, data in all_data.items():
            for record in data.get("records", []):
                if record.get("type") == "A" and record.get("destination") == target_ip:
                    matching.append({
                        "domain": domain,
                        "hostname": record.get("hostname", "@"),
                        "record": record
                    })
        
        return matching
    
    def __enter__(self):
        """Context manager entry - auto login"""
        self.login()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto logout"""
        self.logout()
        return False
