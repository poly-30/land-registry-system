const express = require('express');
const router = express.Router();
const { callBlockchain } = require('../utils/pythonBridge');
const { authenticateToken } = require('../middleware/auth');

// Get all properties
router.get('/', async (req, res) => {
  try {
    const data = await callBlockchain('get_properties');
    res.json(data.properties || []);
  } catch (error) {
    console.error("Properties error:", error.message);
    res.status(500).json({ message: "Failed to fetch properties" });
  }
});

// Register a new property (requires auth)
router.post('/register', authenticateToken, async (req, res) => {
  try {
    const { property_id, details } = req.body;
    
    // The owner address could be linked to the user's wallet
    // For now, we'll use the user's email as a mock address if wallet isn't implemented
    const owner_address = req.user.walletAddress || req.user.email;

    const data = await callBlockchain('register_property', {
      property_id,
      owner_address,
      details
    });

    if (data.error) {
      return res.status(400).json({ message: data.error });
    }

    res.status(201).json(data);
  } catch (error) {
    console.error("Property registration error:", error.message);
    res.status(500).json({ message: "Failed to register property" });
  }
});

module.exports = router;
