import subprocess
import random
import time

vpn_servers = [
    {"country_code": "se", "city_code": "mma"},  # Malmö, Sweden
    {"country_code": "us", "city_code": "nyc"},  # New York, USA
    {"server_code": "se-mma-wg-001"},           # Specific server in Malmö, Sweden
    {"country_code": "de", "city_code": "ber"},  # Berlin, Germany
    {"country_code": "gb", "city_code": "lon"},  # London, UK
    {"country_code": "ca", "city_code": "tor"},  # Toronto, Canada
    {"country_code": "au", "city_code": "syd"},  # Sydney, Australia
    {"country_code": "fr", "city_code": "par"},  # Paris, France
    {"country_code": "jp", "city_code": "tok"},  # Tokyo, Japan
    {"country_code": "nl", "city_code": "ams"},  # Amsterdam, Netherlands
    {"country_code": "ch", "city_code": "zur"},  # Zurich, Switzerland
    {"server_code": "us-nyc-wg-003"},           # Specific server in New York, USA
    {"server_code": "nl-ams-wg-004"},           # Specific server in Amsterdam, Netherlands
    {"country_code": "it", "city_code": "mil"},  # Milan, Italy
    {"country_code": "es", "city_code": "mad"},  # Madrid, Spain
    {"country_code": "no", "city_code": "osl"},  # Oslo, Norway
    {"country_code": "se", "city_code": "sto"},  # Stockholm, Sweden
    {"country_code": "fi", "city_code": "hel"},  # Helsinki, Finland
    {"country_code": "at", "city_code": "vie"},  # Vienna, Austria
    {"country_code": "pl", "city_code": "war"},  # Warsaw, Poland
    {"country_code": "ru", "city_code": "msk"},  # Moscow, Russia
    {"country_code": "sg", "city_code": "sin"},  # Singapore
    {"country_code": "hk", "city_code": "hk"},   # Hong Kong
    {"country_code": "in", "city_code": "del"},  # Delhi, India
    {"country_code": "br", "city_code": "sao"},  # São Paulo, Brazil
    {"country_code": "za", "city_code": "joh"},  # Johannesburg, South Africa
]



def connect_vpn(country_code=None, city_code=None, server_code=None):
    """Connect to a specific Mullvad VPN server."""
    if server_code:
        command = f"mullvad relay set location {server_code}"
    elif country_code and city_code:
        command = f"mullvad relay set location {country_code} {city_code}"
    elif country_code:
        command = f"mullvad relay set location {country_code}"
    else:
        command = "mullvad relay set location any"
    subprocess.run(command.split())
    subprocess.run(["mullvad", "connect"])
    time.sleep(5)

def disconnect_vpn():
    """Disconnect the VPN."""
    subprocess.run(["mullvad", "disconnect"])

def connect_to_vpn():
    connect_vpn(**random.choice(vpn_servers)) 

# def main():
#     for server in vpn_servers:
#         print(f"Connecting to VPN: {server}")
#         connect_vpn(**server)  
#         time.sleep(5)

#         # disconnect_vpn()

# if __name__ == "__main__":
#     main()