const express = require("express");
const router = express.Router();
const protect = require("../middleware/authMiddleware");
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

router.get("/me", protect, async (req, res) => {
    try {
        const user = await prisma.user.findUnique({
            where: {
                id: req.user.id
            },
            select: {
                id: true,
                name: true,
                email: true
            }
        });

        if (!user) {
            return res.status(404).json({
                message: "User not found"
            });
        }

        return res.status(200).json({
            message: "Profile fetched successfully",
            user
        });

    } catch (error) {
        return res.status(500).json({
            message: "Server error",
            error: error.message
        });
    }
});

module.exports = router;