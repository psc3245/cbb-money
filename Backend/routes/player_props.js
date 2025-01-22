const mongoose = require('mongoose');

const stats = {
    Points: "PNT",
    Assists: "AST",
    Rebounds: "REB",
    PointsAndRebounds: "P+R",
    PointsAndAssists: "P+A",
    AssistsAndRebounds: "A+R",
    PointsAssistsRebounds: "PRA",
    Turnovers: "TOV",
    ThreePointsMade: "3PM",
    FieldGoalsMade: "FGM",
    Steal: "STL",
    Block: "BLK"
};

/*
The though process:
Game: the game we are betting on
Party: player we are betting on
Line: The numerical goal, regardless of direction
Stat: The statistic being measured and compared to the line
Result: The condition for a bet to be a win
Odds: odds
*/

const player_prop_schema = new mongoose.Schema({
    game: {
        type: String,
        required: true
    },
    party: {
        type: String,
        required: true
    },
    line: {
        type: double,
        required: true
    },
    stat: {
        type: stats,
        required: true
    },
    result: {
        type: String,
        required: true
    },
    odds: {
        type: int,
        required: true
    }
});

module.exports = mongoose.model('Player_Props', player_prop_schema);