//File: static/js/realtime.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = io({
        transports: ['websocket'],
        upgrade: false
    });
    
    // Simulated sensor data (replace with actual IoT sensor data)
    function sendSensorData() {
        const sensorData = {
            pressure: Math.random() * 100,
            load: Math.random() * 1000,
            wheel_rotations: Math.floor(Math.random() * 1000),
            parking_brake: Math.random() > 0.5
        };
        
        socket.emit('sensor_update', sensorData);
    }
    
    // Simulate sensor updates every 5 seconds
    setInterval(sendSensorData, 5000);
    
    // Complete cycle button
    document.getElementById('complete-cycle').addEventListener('click', () => {
        fetch('/complete_cycle', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(`Cycle Complete. 
                        TKPH: ${data.tkph}
                        Loaded Distance: ${data.loaded_distance} km
                        Unloaded Distance: ${data.unloaded_distance} km
                        Average Speed: ${data.avg_speed} km/h`);
                }
            });
    });
});