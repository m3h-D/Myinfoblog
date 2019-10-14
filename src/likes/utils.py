PRIVATE_IPS_PREFIX = ('10.', '192.', '172.',)


def get_client_ip(request):
    """ip kasi ke dare request mide ro begir"""
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop[0]
        if len(proxies) > 0:
            ip = proxies[0]

    return ip