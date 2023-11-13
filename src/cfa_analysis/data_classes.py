from dataclasses import dataclass


@dataclass
class Indicator:
    abbrv: str
    description: str
    label: str = None
    unit: str = None
    source: str = None
