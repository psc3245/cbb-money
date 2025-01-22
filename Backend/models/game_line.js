const mongoose = require('mongoose');

// ENUM bet_type
const bet_type = {
    Moneyline: "Moneyline",
    Spread: "Spread",
    Point_Total: "PointTotal",
}
// Thoughts:
// A betting line is composed of:
/* 
The game, formatted as TEAM1@TEAM2
The bet type, see enum above
The party, this can be the player in a player prop, 
The result, or what causes the bet to win, i.e. o3.5 rebounds
The odds, i.e. positive number for plus and negative number for minus odds
*/
const game_odds_schema = new mongoose.Schema({
    game: {
        type: String,
        required: true
    },
    betType: {
        type: bet_type,
        required: true
    },
    party: {
        type: String,
        required: true
    },
    result: {
        type: String,
        required: false
    },
    odds: {
        type: int,
        required: true
    }
});

module.exports = mongoose.model('Game_Lines', game_odds_schema);