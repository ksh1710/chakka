from dataclasses import dataclass
from datetime import datetime

@dataclass
class TyreData:
    """
    Represents real-time tyre sensor data
    """
    timestamp: datetime
    pressure: float
    load: float
    wheel_rotations: int
    wheel_circumference: float  # in meters
    parking_brake: bool = False

@dataclass
class TyreCycle:
    """
    Represents a complete tyre usage cycle
    """
    start_time: datetime
    end_time: datetime
    loading_time: float  # hours
    unloading_time: float  # hours
    load_weight: float  # tonnes
    loaded_distance: float  # kilometers
    unloaded_distance: float  # kilometers
    avg_speed: float  # kilometers per hour
    tkph: float  # Tonnes Kilometers Per Hour