const express = require("express");
const axios = require("axios");
const app = express();
app.use(express.json());

const BLOCKCHAIN_SERVICE_URL = "http://localhost:5000";

app.get("/api/chain", async (req, res) => {
    try {
      const response = await axios.get(`${BLOCKCHAIN_SERVICE_URL}/chain`);
      res.json(response.data);
    } catch (error) {
      console.error("Error fetching chain:", error.message);
      res.status(500).json({ error: "Error fetching chain" });
    }
});

app.post("/api/addBlock", async (req, res) => {
    const data = req.body.data;
      if (!data) {
        return res.status(400).json({ error: "Data is missing" });
      }
        try {
          const response = await axios.post(`${BLOCKCHAIN_SERVICE_URL}/add_block`, { data });
          res.json(response.data);
        } catch (error) {
          console.error("Error adding block:", error.message);
          res.status(500).json({ error: "Error adding block" });
        }
});


const PORT = process.env.PORT || 5100;
    app.listen(PORT, () => {
      console.log(`API server listening on port ${PORT}`);
    });