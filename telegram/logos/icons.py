from dataclasses import dataclass


@dataclass(frozen=True)
class Icons:
    GITHUB: str = "https://raw.githubusercontent.com/wkpn/wkpnbot/master/telegram/logos/github.png"
    LINKEDIN: str = "https://raw.githubusercontent.com/wkpn/wkpnbot/master/telegram/logos/linkedin.png"
    PROTONMAIL: str = "https://raw.githubusercontent.com/wkpn/wkpnbot/master/telegram/logos/pm.png"
    SIGNAL: str = "https://raw.githubusercontent.com/wkpn/wkpnbot/master/telegram/logos/signal.png"
