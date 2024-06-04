const { Kafka } = require('kafkajs');
const { spawn } = require('child_process');

// Kafka configuration
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'indicator-group' });

const runConsumer = async () => {
  // Connect the consumer
  await consumer.connect();

  // Subscribe to all topics
  const topics = ['1 min', '5 min', '15 min', '30 min'];
  for (const topic of topics) {
    await consumer.subscribe({ topic, fromBeginning: true });
  }

  // Run the consumer
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = JSON.parse(message.value.toString());
      const { stock_id, time_frame } = data;

      console.log(`Received message from topic ${topic}: Stock ID: ${stock_id}, Time Frame: ${time_frame}`);

      // Call Python script for processing
      const pythonProcess = spawn('python3', ['process_data.py', JSON.stringify(data)]);

      pythonProcess.stdout.on('data', (output) => {
        console.log(`Processed data: ${output.toString()}`);
        // Here you can send the processed data back to Kafka or another service
      });

      pythonProcess.stderr.on('data', (error) => {
        console.error(`Error from Python script: ${error.toString()}`);
      });

      pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
      });
    },
  });
};

runConsumer().catch(console.error);
