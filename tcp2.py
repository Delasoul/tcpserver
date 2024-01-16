import socket
import json
import subprocess
import sys

# Function to process weather data and extract specific information
def process_weather_data(weather_data):
    temperature = weather_data.get('current_weather', {}).get('temperature')
    windspeed = weather_data.get('current_weather', {}).get('windspeed')
    last_update_time = weather_data.get('current_weather', {}).get('time')

    return temperature, windspeed, last_update_time

# Function to get weather data using getweatherAPI.py script
def get_weather_from_api():
    try:
        # Get the path to the Python executable
        python3_executable = sys.executable

        # Run the getweatherAPI.py script
        result = subprocess.run([python3_executable, 'getweatherAPI.py'], capture_output=True, text=True)

       ## print("getweatherAPI.py output:", result.stdout)  # Add this line for debugging

        weather_data = json.loads(result.stdout)
        return weather_data
    except Exception as e:
        print(f"Error fetching weather data from API: {e}")
        return {}

# Define the server address (host, port)
host = 'localhost'
port = 12300

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the socket option to reuse the address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections (max queue of 5)
server_socket.listen(10)

print(f"Server listening on {host}:{port}")

# Dictionary to store weather data
stored_weather_data = {}

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        # Receive data from the client
        data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk

            # Attempt to decode received data line by line
            lines = data.decode('utf-8', errors='ignore').split('\n')
            for line in lines[:-1]:  # Process all complete lines
                if not line:
                    continue  # Skip empty lines

                print(f"Received line: {line}") #Debug to see when and what line was recieved

                if line.strip() == "GET_TEMP":
                    # Check if 'temperature' key is present in stored data
                    if 'temperature' in stored_weather_data:
                        response_data = {'temperature': stored_weather_data['temperature']}
                    else:
                        # Use getweatherAPI.py to fetch weather data
                        weather_data_from_api = get_weather_from_api()
                        temperature, _, _ = process_weather_data(weather_data_from_api)
                        stored_weather_data['temperature'] = temperature
                        response_data = {'temperature': temperature}

                    # Send back the response data as a JSON response
                    response_data_json = json.dumps(response_data)
                    client_socket.send(response_data_json.encode('utf-8'))

                elif line.strip() == "GET_WINDSPEED":
                    # Check if 'windspeed' key is present in stored data
                    if 'windspeed' in stored_weather_data:
                        response_data = {'windspeed': stored_weather_data['windspeed']}
                    else:
                        # Use getweatherAPI.py to fetch weather data
                        weather_data_from_api = get_weather_from_api()
                        _, windspeed, _ = process_weather_data(weather_data_from_api)
                        stored_weather_data['windspeed'] = windspeed
                        response_data = {'windspeed': windspeed}

                    # Send back the response data as a JSON response
                    response_data_json = json.dumps(response_data)
                    client_socket.send(response_data_json.encode('utf-8'))

                else:
                    # Handle other commands or non-JSON data
                    print("Received command:", line)

    except Exception as e:
        print(f"Error processing data: {e}")

    finally:
        # Close the client socket
        client_socket.close()
