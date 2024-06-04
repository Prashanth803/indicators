const WebSocket = require('ws');
const faker = require('faker');

const ws = new WebSocket('ws://localhost:8080');

// Function to generate fake data
const generateFakeData = () => {
  const timeFrames = ['1 min', '5 min', '15 min', '30 min'];
  return {
    stock_id: faker.finance.currencyCode(),
    time_frame: timeFrames[Math.floor(Math.random() * timeFrames.length)],
    value: faker.finance.amount(),
    timestamp: new Date().toISOString()
  };
};

ws.on('open', () => {
  console.log('Connected to WebSocket server');

  // Send fake data every second
  setInterval(() => {
    const data = generateFakeData();
    ws.send(JSON.stringify(data));
    console.log('Sent data:', data);
  }, 1000);
});

ws.on('message', (message) => {
  console.log('Received from server:', message);
});

ws.on('close', () => {
  console.log('Disconnected from WebSocket server');
});

ws.on('error', (error) => {
  console.error('WebSocket error:', error);
});
