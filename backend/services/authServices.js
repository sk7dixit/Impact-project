const bcrypt = require("bcrypt");
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

const findUserByEmail = async (email) => {
    return await prisma.user.findUnique({
        where: {
            email
        }
    });
};

const createUser = async (name, email, password) => {
    const hashedPassword = await bcrypt.hash(password, 10);

    return await prisma.user.create({
        data: {
            name,
            email,
            password: hashedPassword
        }
    });
};

const comparePassword = async (password, hashedPassword) => {
    return await bcrypt.compare(password, hashedPassword);
};

module.exports = {
    findUserByEmail,
    createUser,
    comparePassword
};