const express = require('express');
const router = express.Router();
const Game_Line = require('../models/game_line');

// Get All Data
router.get('/', async (req, res) => {
    try {
        const game_lines = await Game_Line.find();
        res.json(game_lines);
    }
    catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Get One
// colon means parameter, access with req.params.id
router.get('/:id', getGameLine, (req, res) => {
    res.json(res.game_line);
});

// Create One
router.post('/', async (req, res) => {
    const game_line = new Game_Line({
        game: req.body.game,
        result: req.body.result,
        odds: req.body.odds
    });

    try {
        const new_game_line = await game_line.save();
        res.status(201).json(new_game_line);

    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Update One
router.patch('/:id', getGameLine, async (req, res) => {
    if (req.body.game != null) {
        res.game_line.game = req.body.game;
    }
    if (req.body.result != null) {
        res.game_line.result = req.body.result;
    }
    if (req.body.odds != null) {
        res.game_line.odds = req.body.odds;
    }
    try {
        const updated_game_line = await res.game_line.save();
        res.json(updated_game_line);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Delete One
router.delete('/:id', getGameLine, async (req, res) => {
    try {
        await res.game_line.deleteOne();
        res.status(204);

    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

async function getGameLine(req, res, next) {
    let game_line;
    try {
        game_line = await Game_Line.findById(req.params.id);
        if (game_line == null) {
            return res.status(404).json({ message: "Could not find game line" });
        }
    }
    catch (err) {
        res.status(500).json({ message: err.message });
    }

    res.game_line = game_line;
    next();
};


module.exports = router;