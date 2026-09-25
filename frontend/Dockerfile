# Use official Node runtime as a parent image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Command to start the frontend
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]