""" DataClasses for data returned from imf query """
from dataclasses import dataclass


@dataclass
class Indicator:
    """Indicator from imf, fields : abbreviation, description, label, unit and source"""

    abbrv: str
    description: str
    label: str = None
    unit: str = None
    source: str = None
