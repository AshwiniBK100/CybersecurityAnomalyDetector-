import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from tkinter import Tk, Label, Button, Text, Scrollbar, END, messagebox
import json

class CybersecurityAnomalyDetector:
    def __init__(self, num_records=1000):
        self.num_records = num_records
        self.data = None
        self.model = None
        self.model_advanced = None
        self.scaler = StandardScaler()
        self.generate_synthetic_data()
        self.train_model()
        self.train_advanced_model()

    def generate_synthetic_data(self):
        """Generates synthetic network traffic data."""
        np.random.seed(42)
        normal_data = {
            'timestamp': pd.date_range(start='2023-01-01', periods=self.num_records, freq='s'),
            'src_ip': ['192.168.1.' + str(np.random.randint(1, 255)) for _ in range(self.num_records)],
            'dst_ip': ['192.168.1.' + str(np.random.randint(1, 255)) for _ in range(self.num_records)],
            'data_size': np.random.normal(loc=1000, scale=100, size=self.num_records),
            'is_attack': 0  # Normal traffic
        }

        normal_df = pd.DataFrame(normal_data)

        # Inject anomalies
        anomaly_records = []
        for _ in range(50):
            anomaly = {
                'timestamp': pd.Timestamp.now() + pd.Timedelta(seconds=np.random.randint(0, 300)),
                'src_ip': '192.168.1.100',
                'dst_ip': '192.168.1.200',
                'data_size': np.random.randint(5000, 10000),
                'is_attack': 1
            }
            anomaly_records.append(anomaly)

        anomaly_df = pd.DataFrame(anomaly_records)
        self.data = pd.concat([normal_df, anomaly_df], ignore_index=True)

    def train_model(self):
        """Trains the basic anomaly detection model using Isolation Forest."""
        X = self.data[['data_size']].values
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.model.fit(X)

    def train_advanced_model(self):
        """Trains a neural network model to detect anomalies."""
        X = self.data[['data_size']].values
        X_scaled = self.scaler.fit_transform(X)  # Scaling the input data

        # Train a neural network (MLPRegressor) for advanced anomaly detection
        self.model_advanced = MLPRegressor(
            hidden_layer_sizes=(10, 5),      # Adjusted hidden layer sizes
            solver='lbfgs',                  # Using the 'lbfgs' solver for better convergence
            learning_rate_init=0.001,        # Fine-tuning the learning rate
            random_state=42,                 # Random state for reproducibility
            max_iter=1000                    # Increased number of iterations to allow convergence
        )
        self.model_advanced.fit(X_scaled, self.data['is_attack'])

    def detect_anomalies(self):
        """Detects anomalies using both models."""
        if self.model is None or self.model_advanced is None:
            raise RuntimeError("Models are not trained. Call train_model() and train_advanced_model() first.")

        X = self.data[['data_size']].values
        X_scaled = self.scaler.transform(X)  # Scaling the input data for advanced model

        # Isolation Forest prediction
        self.data['anomaly_if'] = self.model.predict(X)
        self.data['anomaly_if'] = self.data['anomaly_if'].apply(lambda x: 1 if x == -1 else 0)

        # MLPRegressor prediction (Advanced Model)
        self.data['anomaly_mlp'] = self.model_advanced.predict(X_scaled)
        self.data['anomaly_mlp'] = np.where(self.data['anomaly_mlp'] > 0.5, 1, 0)

        # Combine the results of both models
        self.data['anomaly'] = np.where((self.data['anomaly_if'] == 1) | (self.data['anomaly_mlp'] == 1), 1, 0)

        anomalies = self.data[self.data['anomaly'] == 1]
        self.save_mock_log(anomalies)  # Save anomalies to JSON
        return anomalies

    def save_mock_log(self, anomalies):
        """Saves the detected anomalies to a JSON file."""
        log_data = anomalies.to_dict(orient='records')
        
        # Convert timestamps to string
        for entry in log_data:
            entry['timestamp'] = entry['timestamp'].isoformat()  # Convert to ISO format
        
        with open('mock_anomaly_logs.json', 'a') as f:
            for entry in log_data:
                f.write(json.dumps(entry) + "\n")

class AnomalyDetectionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Cybersecurity Anomaly Detector")

        self.label = Label(master, text="Click the button to detect anomalies:")
        self.label.pack(pady=10)

        self.detect_button = Button(master, text="Detect Anomalies", command=self.detect_anomalies, bg='green', fg='white', width=20)
        self.detect_button.pack(pady=5)

        self.results_text = Text(master, wrap='word', width=70, height=20, bg='lightgray')
        self.results_text.pack(pady=10)

        self.scrollbar = Scrollbar(master, command=self.results_text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=self.scrollbar.set)

        self.detector = CybersecurityAnomalyDetector()

    def detect_anomalies(self):
        try:
            anomalies = self.detector.detect_anomalies()
            self.results_text.delete(1.0, END)  # Clear previous results

            if not anomalies.empty:
                response = f"**Threat Detected!**\n\n"
                response += f"Total Anomalies Detected: {len(anomalies)}\n\n"
                response += "Details of Detected Anomalies:\n"
                response += "-----------------------------------\n"

                for index, anomaly in anomalies.iterrows():
                    response += (
                        f"Timestamp: {anomaly['timestamp']}\n"
                        f"Source IP: {anomaly['src_ip']}\n"
                        f"Destination IP: {anomaly['dst_ip']}\n"
                        f"Data Size: {anomaly['data_size']} bytes\n"
                        f"Is Attack: {'Yes' if anomaly['is_attack'] else 'No'}\n"
                        "-----------------------------------\n"
                    )
            else:
                response = "No threats detected."
               
            self.results_text.insert(END, response)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    root = Tk()
    gui = AnomalyDetectionGUI(root)
    root.mainloop()
