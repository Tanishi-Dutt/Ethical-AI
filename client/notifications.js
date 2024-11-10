<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Real-Time Monitoring Client</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <h1>Real-Time Monitoring Client</h1>

    <button onclick="simulateTransaction()">Simulate Transaction</button>
    <button onclick="simulateCommunication('call')">Simulate Call</button>
    <button onclick="simulateCommunication('message')">Simulate Message</button>
    <button onclick="simulateCommunication('email')">Simulate Email</button>

    <script>
        // Establish socket connection
        const socket = io('http://localhost:5000');

        // Display alert messages from server
        socket.on('alert', (data) => {
            alert(`Alert: ${data.message}`);
        });

        // Function to simulate a transaction
        function simulateTransaction() {
            fetch('http://localhost:5000/transaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 'user123',
                    amount: Math.floor(Math.random() * 10000) // Random amount for testing
                })
            })
            .then(response => response.json())
            .then(data => alert(`Transaction Status: ${data.status}`))
            .catch(error => console.error('Error:', error));
        }

        // Function to simulate communication (call, message, or email)
        function simulateCommunication(type) {
            fetch('http://localhost:5000/communication', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: type,
                    identifier: type === 'email' ? 'test@example.com' : '+1234567890' // Test data
                })
            })
            .then(response => response.json())
            .then(data => alert(`Communication Status: ${data.status}`))
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
