const express = require('express');
const router = express.Router();
const { callBlockchain } = require('../utils/pythonBridge');

router.get('/chain', async (req, res) => {
  try {
    const chainData = await callBlockchain('get_chain');
    res.json(chainData);
  } catch (error) {
    console.error("Blockchain chain error:", error.message);
    res.status(500).json({ message: "Failed to fetch blockchain data" });
  }
});

module.exports = router;
