import ipaddress

from fastapi import HTTPException


def tuple_to_string(address):
    result = ', '.join(map(str, address))
    result = result.replace('(', '').replace(')', '')
    return result


def check_user_ip(user_ip: str, ip_whitelist) -> bool:
    for ip in ip_whitelist:
        ip = tuple_to_string(ip)
        if '/' in ip:
            try:
                ip = ipaddress.ip_address(user_ip)
                network = ipaddress.ip_network(ip, strict=False)
                if ip in network:
                    return True
            except ValueError:
                raise HTTPException(status_code=403, detail="Invalid IP address.")
        elif user_ip == ip:
            return True
    return False
