const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const authRoutes = require("./routes/authRoutes");
const userRoutes = require("./routes/userRoutes");
const aiRoutes = require("./routes/aiRoutes");
const errorHandler = require("./middleware/errorMiddleware");
dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());
app.use("/api/auth",authRoutes);
app.use("/api/users",userRoutes);
app.use("/api/ai", aiRoutes);
app.use(errorHandler);
const PORT = process.env.PORT || 5000;
app.get("/" , (req , res) => {
    res.send("Backend Server Running");
});
app.listen(PORT , () => {
    console.log(`Server running on port ${PORT}`);
}); 