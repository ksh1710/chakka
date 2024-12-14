# File: app/calculations.py
import math
from datetime import datetime

class TyreCalculator:
    @staticmethod
    def calculate_tkph(load_weight, distance, time):
        """
        Calculate Tonnes Kilometer Per Hour (TKPH)
        
        Args:
            load_weight (float): Weight of the load in tonnes
            distance (float): Distance traveled in kilometers
            time (float): Total time in hours
        
        Returns:
            float: TKPH value
        """
        if time == 0:
            return 0
        
        tkph = (load_weight * distance) / time
        return round(tkph, 2)

    @staticmethod
    def calculate_distance(wheel_rotations, wheel_circumference):
        """
        Calculate distance traveled based on wheel rotations
        
        Args:
            wheel_rotations (int): Number of wheel rotations
            wheel_circumference (float): Circumference of the wheel in meters
        
        Returns:
            float: Distance traveled in kilometers
        """
        # Convert meters to kilometers
        distance_km = (wheel_rotations * wheel_circumference) / 1000
        return round(distance_km, 2)

    @staticmethod
    def calculate_avg_speed(total_distance, total_time):
        """
        Calculate average speed
        
        Args:
            total_distance (float): Total distance traveled in kilometers
            total_time (float): Total time in hours
        
        Returns:
            float: Average speed in km/h
        """
        if total_time == 0:
            return 0
        
        avg_speed = total_distance / total_time
        return round(avg_speed, 2)