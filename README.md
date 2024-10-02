# CybersecurityAnomalyDetector
# CybersecurityAnomalyDetector

## Tagline
An AI-driven solution for autonomously detecting and responding to cybersecurity threats in real time at the end-user level.

## Description
The Cybersecurity Anomaly Detector leverages advanced machine learning models to autonomously detect, analyze, and respond to potential cybersecurity threats. By processing vast amounts of data from network traffic, user behavior, and system logs, the solution identifies unusual patterns or anomalies that may indicate a security breach.

### In-Scope Features
- **Data Generation**: Generates synthetic network traffic data for testing and demonstration purposes.
- **Anomaly Detection**: Utilizes Isolation Forest and MLPRegressor models to detect anomalies in the generated data.
- **Result Reporting**: Displays detected anomalies in a user-friendly GUI.
- **Log Saving**: Saves detected anomalies to a JSON file for further analysis.

### Out of Scope Features
- Real-time integration with live systems or production environments.
- Direct integration with Security Information and Event Management (SIEM) systems (due to lack of IT support).
- Advanced features such as automated response actions and detailed user behavior analytics.

### Future Opportunities
- Integration with existing SIEM systems for real-time threat detection and response.
- Enhancements to the machine learning models to improve detection accuracy.
- Development of a web-based interface for broader accessibility.
- Implementation of automated response mechanisms to mitigate detected threats.

## Challenges We Ran Into
- **SIEM Integration**: Unable to integrate with a SIEM system due to lack of IT support. This limited the real-time functionality of the solution.
- **Authentication Mechanisms**: Implementing API key or OAuth 2.0 authentication for secure access to the SIEM system was challenging without actual credentials.
- **Testing with Actual Placeholders**: It would be helpful to replace placeholders with actual SIEM system endpoints during testing to ensure proper functionality.

## Technologies Used
- Python
- Scikit-learn
- Pandas
- NumPy
- Tkinter (for GUI)

