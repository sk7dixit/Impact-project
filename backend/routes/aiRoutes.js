const express = require("express");
const router = express.Router();
const protect = require("../middleware/authMiddleware");

router.post("/chat", protect, async (req, res) => {
    try {
        const { message } = req.body;

        if (!message) {
            return res.status(400).json({
                message: "Message is required"
            });
        }

        const aiPayload = {
            userId: req.user.id,
            query: message
        };

        // MOCK AI SERVICE RESPONSE (temporary)
        const aiResponse = {
            answer: `AI received: ${message}`,
            confidence: 0.95
        };

        res.status(200).json({
            message: "AI request processed successfully",
            input: aiPayload,
            response: aiResponse
        });

    } catch (error) {
        res.status(500).json({
            message: "Server error",
            error: error.message
        });
    }
});

module.exports = router;