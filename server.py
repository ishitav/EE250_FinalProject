import socket
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
import threading


HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 65432
BUFFER_SIZE = 1024
print("Listening on " + str(HOST) + ":" + str(PORT))

data_queue = Queue()

def update_plot(frame):
    global volume_levels, freq_levels, index
    while not data_queue.empty():
        volume, freq = data_queue.get().split(',')
        volume_levels[index % 100] = float(volume)
        freq_levels.append(float(freq))
        index += 1
    volume_line.set_ydata(volume_levels)
    freq_line.set_ydata(freq_levels)
    freq_line.set_xdata(range(len(freq_levels)))
    ax2.relim()
    ax2.autoscale_view()
    return volume_line, freq_line

def receive_volume_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(BUFFER_SIZE).decode()
                if not data:
                    break
                data_queue.put(data)

if __name__ == "__main__":
    volume_levels = [0] * 100  # volume levels list
    freq_levels = []  # frequency levels list as an empty list
    index = 0  # index for volume list management

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title('Volume Level')
    ax2.set_title('Frequency Over Time')
    ax1.set_ylim(0, 100)
    x = range(100)
    volume_line, = ax1.plot(x, volume_levels)
    freq_line, = ax2.plot([], [])  

    ani = FuncAnimation(fig, update_plot, blit=True, interval=100)

    print("Starting server thread...")
    thread = threading.Thread(target=receive_volume_data)
    thread.start()

    plt.show()
    print("Closing server...")
    thread.join()

