require('dotenv').config();

const express = require('express');
const app = express();
const mongoose = require('mongoose');

mongoose.connect(process.env.DATABASE_URL);
const db = mongoose.connection;
db.on('error', (error) => console.error(error));
db.once('open', () => console.log('Connected to Database'));

app.use(express.json());

// This line creates a variable that acts as the directions for where data should go
const dataRouter = require('./routes/game_lines');
// This line tells the rest api where to send data for processing
app.use('/game_lines', dataRouter);

app.listen(3000, () => console.log('Server Started'));