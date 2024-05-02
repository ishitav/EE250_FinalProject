import socket
import numpy as np
import sounddevice as sd

def audio_callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    # Calculate the RMS of the audio sample for volume
    volume_norm = np.linalg.norm(indata) * 10
    # FFT transformation
    fft_data = np.fft.rfft(indata.flatten())  # Apply FFT on flattened array
    fft_magnitude = np.abs(fft_data)  # Get magnitude
    dominant_freq = np.argmax(fft_magnitude)  # Find dominant frequency
    # Send both volume and frequency data
    client_socket.sendall(f"{volume_norm},{dominant_freq}".encode())

# Configure the IP address of the server and the port number
HOST = '192.168.0.206' 
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print("Attempting to connect to the server...")
    client_socket.connect((HOST, PORT))
    print("Connection successful!")
    with sd.InputStream(callback=audio_callback):
        input("Press Enter to stop the client...\n")
    print("Shutting down client...")

