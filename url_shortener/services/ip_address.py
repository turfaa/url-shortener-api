import ipaddress

from rest_framework.request import Request

PRIVATE_IP_PREFIXES = ('10.', '172.', '192.', '127.')


class IpAddressService:
    def __init__(self, request: Request = None) -> None:
        self.request = request

    def is_valid_ip(self, ip_address: str) -> bool:
        try:
            ipaddress.ip_address(u'' + ip_address)
            return True
        except ValueError:
            return False

    def get_ip_address(self) -> str:
        if self.request is None:
            raise Exception('Request is not defined')
        
        ip_address = ''
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR', '')

        if x_forwarded_for and ',' not in x_forwarded_for:
            if not x_forwarded_for.startswith(PRIVATE_IP_PREFIXES) and self.is_valid_ip(x_forwarded_for):
                ip_address = x_forwarded_for.strip()
        else:
            ips = [ip.strip() for ip in x_forwarded_for.split(',')]
            for ip in ips:
                if ip.startswith(PRIVATE_IP_PREFIXES):
                    continue
                elif not self.is_valid_ip(ip):
                    continue
                else:
                    ip_address = ip
                    break

        if not ip_address:
            x_real_ip = self.request.META.get('HTTP_X_REAL_IP', '')
            if x_real_ip:
                if not x_real_ip.startswith(PRIVATE_IP_PREFIXES) and self.is_valid_ip(x_real_ip):
                    ip_address = x_real_ip.strip()

        if not ip_address:
            remote_addr = self.request.META.get('REMOTE_ADDR', '')
            if remote_addr:
                if not remote_addr.startswith(PRIVATE_IP_PREFIXES) and self.is_valid_ip(remote_addr):
                    ip_address = remote_addr.strip()

        if not ip_address:
            ip_address = '127.0.0.1'

        return ip_address
