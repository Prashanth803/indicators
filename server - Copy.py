import socket
import pickle
import ovbv
import rsi
import pandas as pd

class DataReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(4096)
                    if not data:
                        break
                    # Unpickle the data
                    data = pickle.loads(data)
                    # Process data with different modules
                    stocks = pd.DataFrame(columns=['symbol','timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    close=200
                    rsi_calulator=rsi.RSI(stocks,close)
                    obv_cakculator=ovbv.OBV(stocks,close)
                    result_a = rsi_calulator.run()
                    result_b=obv_cakculator.run()
                    # Serialize the results (DataFrames)
                    serialized_result_a = pickle.dumps(result_a)
                    serialized_result_b = pickle.dumps(result_b)
                    # Pack the results
                    results = {
                        "result_a": serialized_result_a,
                        "result_b": serialized_result_b,
                    }
                    # Send back the results
                    conn.sendall(pickle.dumps(results))

if __name__ == "__main__":
    receiver = DataReceiver("localhost", 5001)  # Listen for incoming data
    receiver.start()
