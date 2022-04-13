from dataclasses import dataclass


logos_path: str = "https://raw.githubusercontent.com/wkpn/wkpnbot/master/telegram/logos/img"


@dataclass(frozen=True)
class Logos:
    GITHUB: str = f"{logos_path}/github.png"
    LINKEDIN: str = f"{logos_path}/linkedin.png"
    PROTONMAIL: str = f"{logos_path}/pm.png"
    SIGNAL: str = f"{logos_path}/signal.png"
