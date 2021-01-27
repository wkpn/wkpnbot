from ipaddress import IPv4Address, IPv4Network
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Optional


TG_NETWORKS = [IPv4Network("149.154.160.0/20"), IPv4Network("91.108.4.0/22")]


def check_ip(request_host: Optional[str]) -> None:
    if request_host is None:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="IP address cannot be empty"
        )

    request_ip = IPv4Address(request_host)

    if not any(request_ip in network for network in TG_NETWORKS):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Bad IP address"
        )
