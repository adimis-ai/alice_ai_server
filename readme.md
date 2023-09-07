# Alice Server

Alice Server is a Python application that serves as the backend for an AI-powered chatbot and conversation handling system. It leverages the power of OpenAI's GPT-3 to generate human-like responses in various contexts.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)

## Introduction

Alice Server is designed to handle AI chatbot interactions and conversation management. It provides functions for generating chatbot prompts, summarizing conversations, and interacting with MongoDB for data storage.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/AliceServer.git
   cd AliceServer
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file (use the provided `.env.template` as a starting point).

4. Run the application:

   ```
   uvicorn main:app --host 0.0.0.0 --port 7000 --reload
   ```

## Usage

Alice Server provides several endpoints for interacting with the chatbot and conversation management. Below are some of the key endpoints:

- `GET /` - Check the server's connectivity.
- `POST /chatbot` - Interact with the AI chatbot by sending user input.
- `POST /davinci` - Directly use the Davinci engine for generating text.

For detailed usage instructions and API documentation, refer to the project's API documentation.

## Project Structure

The project is organized as follows:

- `main.py`: The main application entry point.
- `Alice/server/`: Contains utility functions and database actions.
- `conversation_handler.py`: Handles conversation summaries and prompts.
- Other Python files for different functionalities.

## Environment Variables

To run Alice Server, you need to set the following environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key.
- (Add any other necessary environment variables here)

Example `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
DB_URI=your_mongodb_uri
PORT=7000
```

Make sure to fill in the actual values for your project.