# **CliMate: An Agri-Weather Coach**

This is a simple demonstration project developed for the **NASA Space Apps Challenge 2024**. The goal is to connect a conversational AI (Large Language Model) with a weather API to provide weather-related insights for agricultural purposes.

## **Project Overview**

**CliMate** is an agri-weather assistant that allows users to ask weather-related questions and get useful information based on real-time data. By combining the power of a natural language model and weather data, CliMate helps users make informed farming decisions.

## **Features**
- Provides weather data for a specific location.
- Offers insights related to precipitation and flooding risks.
- Simple conversation-based interaction.

## **Tech Stack**
- **Python**: Main programming language.
- **OpenAI API**: For the Large Language Model (LLM).
- **METEOMATICS API**: For retrieving weather data.

## **Setup and Installation**

### **Requirements**
- Python 3.8 or higher.
- API keys for OpenAI (ChatGPT) and METEOMATICS.

### **Steps**
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/CliMate-Demo.git
    cd CliMate-Demo
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your API keys:
    ```
    METEOMATICS_USERNAME=your_meteomatics_username
    METEOMATICS_PASSWORD=your_meteomatics_password
    CHATGPT_API_KEY=your_chatgpt_api_key
    ```

4. Run the program:
    ```bash
    python main.py
    ```

## **How It Works**

1. Start the program and interact with the CliMate assistant.
2. Enter a location (city and country), and the assistant will fetch weather data.
3. Get insights based on precipitation levels for farming.

## **Contributing**

This project is for demonstration purposes, but contributions are welcome! Feel free to fork, make changes, and submit a pull request.

## **License**

This project is licensed under the MIT License.
