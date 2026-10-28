// src/middleware/auth.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, payload) => {
    if (err) return res.sendStatus(403);
    // attach user info
    req.user = { id: payload.sub, email: payload.email, role: payload.role };
    next();
  });
}

module.exports = { authenticateToken };
