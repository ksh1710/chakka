# File: app/routes.py
from flask import render_template, jsonify, request
from flask_socketio import emit
from app import socketio  # Import the socketio from __init__
from .firebase_config import init_firebase
from .calculations import TyreCalculator
from .models import TyreData, TyreCycle
from datetime import datetime

# Initialize Firebase
firestore_client, firebase_ref = init_firebase()

# Global variables to track tyre cycle
current_cycle = None
tyre_cycles = []

# Wheel configuration (this should be set based on your specific wheel)
WHEEL_CIRCUMFERENCE = 2.0  # meters, adjust according to your wheel size

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('sensor_update')
def handle_sensor_update(data):
    """
    Handle real-time sensor data updates
    
    Expected data format:
    {
        'pressure': float,
        'load': float,
        'wheel_rotations': int,
        'parking_brake': bool
    }
    """
    global current_cycle
    
    # Create TyreData instance
    tyre_data = TyreData(
        timestamp=datetime.now(),
        pressure=data['pressure'],
        load=data['load'],
        wheel_rotations=data['wheel_rotations'],
        wheel_circumference=WHEEL_CIRCUMFERENCE,
        parking_brake=data['parking_brake']
    )
    
    # Store in Firebase
    firestore_client.collection('tyre_sensor_data').add(vars(tyre_data))
    
    # Cycle Management Logic
    if current_cycle is None:
        # Start a new cycle if parking brake is off and load exists
        if not data['parking_brake'] and data['load'] > 0:
            current_cycle = TyreCycle(
                start_time=datetime.now(),
                loading_time=0,
                unloading_time=0,
                load_weight=data['load'],
                loaded_distance=0,
                unloaded_distance=0,
                avg_speed=0,
                end_time=None,
                tkph=0
            )
    else:
        # Calculate time since cycle start
        total_time = (datetime.now() - current_cycle.start_time).total_seconds() / 3600  # convert to hours
        
        # Loading Condition
        if data['parking_brake'] and data['load'] > current_cycle.load_weight:
            current_cycle.loading_time += (datetime.now() - current_cycle.start_time).total_seconds() / 3600
        
        # Unloading Condition
        if data['parking_brake'] and data['load'] < current_cycle.load_weight:
            current_cycle.unloading_time += (datetime.now() - current_cycle.start_time).total_seconds() / 3600
        
        # Calculate distances
        distance = TyreCalculator.calculate_distance(
            data['wheel_rotations'], 
            WHEEL_CIRCUMFERENCE
        )
        
        # Determine if loaded or unloaded distance
        if data['load'] > 0:
            current_cycle.loaded_distance += distance
        else:
            current_cycle.unloaded_distance += distance
        
        # Calculate average speed
        current_cycle.avg_speed = TyreCalculator.calculate_avg_speed(
            current_cycle.loaded_distance + current_cycle.unloaded_distance, 
            total_time
        )

@socketio.on('complete_cycle')
def handle_complete_cycle():
    global current_cycle, tyre_cycles
    
    if current_cycle:
        # Calculate total distance
        total_distance = current_cycle.loaded_distance + current_cycle.unloaded_distance
        
        # Calculate total time
        total_time = (datetime.now() - current_cycle.start_time).total_seconds() / 3600
        
        # Calculate TKPH
        current_cycle.tkph = TyreCalculator.calculate_tkph(
            current_cycle.load_weight,
            current_cycle.loaded_distance,  # Use loaded distance for TKPH
            total_time
        )
        
        # Store cycle in Firebase
        firestore_client.collection('tyre_cycles').add(vars(current_cycle))
        
        # Add to local cycles list
        tyre_cycles.append(current_cycle)
        
        # Prepare response data
        cycle_data = {
            'status': 'success',
            'tkph': current_cycle.tkph,
            'loaded_distance': current_cycle.loaded_distance,
            'unloaded_distance': current_cycle.unloaded_distance,
            'avg_speed': current_cycle.avg_speed,
            'total_time': total_time
        }
        
        # Emit the cycle data back to the client
        socketio.emit('cycle_completed', cycle_data)
        
        # Reset current cycle
        current_cycle = None
    else:
        socketio.emit('cycle_completed', {'status': 'error', 'message': 'No active cycle'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')



def init_routes(app):
    """
    Initialize routes for the Flask app
    This allows us to keep routes separate from app creation
    """
    @app.route('/')
    def index():
        return render_template('index.html')

    # You can add more traditional routes here if needed
    @app.route('/complete_cycle', methods=['POST'])
    def complete_cycle_route():
        # This is a fallback for traditional HTTP requests
        global current_cycle, tyre_cycles
        
        if current_cycle:
            # Similar logic to handle_complete_cycle
            total_time = (datetime.now() - current_cycle.start_time).total_seconds() / 3600
            
            current_cycle.tkph = TyreCalculator.calculate_tkph(
                current_cycle.load_weight,
                current_cycle.loaded_distance,
                total_time
            )
            
            firestore_client.collection('tyre_cycles').add(vars(current_cycle))
            tyre_cycles.append(current_cycle)
            
            cycle_data = {
                'status': 'success',
                'tkph': current_cycle.tkph,
                'loaded_distance': current_cycle.loaded_distance,
                'unloaded_distance': current_cycle.unloaded_distance,
                'avg_speed': current_cycle.avg_speed,
                'total_time': total_time
            }
            
            current_cycle = None
            return jsonify(cycle_data)
    
        
        return jsonify({'status': 'error', 'message': 'No active cycle'})
@socketio.on_error()
def error_handler(e):
    print(f'An error occurred: {str(e)}')
    socketio.emit('error', {'message': str(e)})