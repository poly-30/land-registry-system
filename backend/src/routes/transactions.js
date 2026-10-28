const express = require('express');
const router = express.Router();
const { callBlockchain } = require('../utils/pythonBridge');

router.post('/transfer', async (req, res) => {
  try {
    const { property_id, to_address, sale_price } = req.body;
    
    const data = await callBlockchain('transfer_ownership', {
      property_id,
      to_address,
      sale_price
    });

    if (data.error) {
      return res.status(400).json({ message: data.error });
    }

    res.status(200).json(data);
  } catch (error) {
    console.error("Transfer error:", error.message);
    res.status(500).json({ message: "Failed to transfer property" });
  }
});

module.exports = router;
