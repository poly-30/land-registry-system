const express = require('express');
const router = express.Router();
const { callBlockchain } = require('../utils/pythonBridge');
const { authenticateToken } = require('../middleware/auth');

// Note: dashboard stats might be public or require auth depending on requirements
// Adding authenticateToken middleware if needed, for now public for easy testing
router.get('/stats', async (req, res) => {
  try {
    const stats = await callBlockchain('get_stats');
    res.json(stats);
  } catch (error) {
    console.error("Dashboard stats error:", error.message);
    res.status(500).json({ message: "Failed to fetch dashboard stats from blockchain" });
  }
});

module.exports = router;
