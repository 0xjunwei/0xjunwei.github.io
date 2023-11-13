// /api/traderjoe.js
const express = require('express');
const axios = require('axios');
const app = express();

app.get('/user-position', async (req, res) => {
  const apiKey = req.query.apiKey; // Get API key from query parameters
  const userAddress = req.query.userAddress; // Get user address from query parameters
  const chain = 'arbitrum';
  const vaultAddress = req.query.vaultAddress; // Get vault address from query parameters

  const traderJoeUrl = `https://api.traderjoexyz.dev/v1/user/${chain}/${userAddress}/farms/${vaultAddress}`;

  try {
    const response = await axios.get(traderJoeUrl, {
      headers: { 'x-traderjoe-api-key': apiKey }
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = app;
