const WebSocket = require('ws');
const { Kafka } = require('kafkajs');

const wss = new WebSocket.Server({ port: 8080 });

// Kafka configuration
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();

const runProducer = async () => {
  await producer.connect();

  wss.on('connection', (ws) => {
    ws.on('message', async (message) => {
      try {
        const data = JSON.parse(message);
        const { time_frame } = data;

        // Determine the topic based on the time frame
        let topic;
        switch (time_frame) {
          case '1 min':
            topic = '1 min';
            break;
          case '5 min':
            topic = '5 min';
            break;
          case '15 min':
            topic = '15 min';
            break;
          case '30 min':
            topic = '30 min';
            break;
          default:
            console.error('Invalid time frame');
            return;
        }

        // Publish the message to the appropriate Kafka topic
        await producer.send({
          topic,
          messages: [
            { value: JSON.stringify(data) }
          ]
        });

        console.log(`Message sent to topic ${topic}: ${message}`);
      } catch (error) {
        console.error('Error processing message:', error);
      }
    });
  });

  console.log('WebSocket server is running on ws://localhost:8080');
};

runProducer().catch(console.error);
