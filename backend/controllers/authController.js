const bcrypt = require("bcrypt");
const generateToken = require("../utils/tokenUtils");
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

const registerUser = async (req, res) => {
    try {
        const { name, email, password } = req.body;

        if (!name || !email || !password) {
            return res.status(400).json({
                message: "All fields are required"
            });
        }

        const existingUser = await prisma.user.findUnique({
            where: { email }
        });

        if (existingUser) {
            return res.status(400).json({
                message: "User already exists"
            });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await prisma.user.create({
            data: {
                name,
                email,
                password: hashedPassword
            }
        });

        const token = generateToken(user.id);

        return res.status(201).json({
            message: "User registered successfully",
            user: {
                name: user.name,
                email: user.email
            },
            token
        });

    } catch (error) {
        return res.status(500).json({
            message: "Server error",
            error: error.message
        });
    }
};

const loginUser = async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({
                message: "Email and password are required"
            });
        }

        const user = await prisma.user.findUnique({
            where: { email }
        });

        if (!user) {
            return res.status(400).json({
                message: "User not found"
            });
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return res.status(400).json({
                message: "Invalid credentials"
            });
        }

        const token = generateToken(user.id);

        return res.status(200).json({
            message: "User logged in Successfully",
            token
        });

    } catch (error) {
        return res.status(500).json({
            message: "Server error",
            error: error.message
        });
    }
};
const logoutUser = async (req, res) => {
    res.status(200).json({
        message: "User logged out successfully"
    });
};

module.exports = {
    registerUser,
    loginUser,
    logoutUser
};