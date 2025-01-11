const mongoose = require('mongoose');

const game_odds_schema = new mongoose.Schema({
    game: {
        type: String,
        required: true
    },
    result: {
        type: String,
        required: true
    },
    odds: {
        type: String,
        required: true
    }
});

module.exports = mongoose.model('Game_Lines', game_odds_schema);