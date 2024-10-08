import os
from dotenv import load_dotenv
from functions import JSON_response
from chatGPT_service import chatgpt_handler
import json
from Meteomatics_Service import EnvironmentLoader


def print_response(response: str):
    """Formats and prints the bot response."""
    formatted_response = "CliMate: " + response + "\n"
    print(formatted_response)

def get_input() -> str:
    """Gets input from the user via console."""
    return input("User: ")

def main():
    """Main logic to handle conversation, fetch data, and process responses."""

    # Initialize EnvironmentLoader
    env_loader = EnvironmentLoader()

    # Access the credentials and variables using the class
    credentials = env_loader.get_credentials()
    chatgpt_api_key = credentials["CHATGPT_API_KEY"]

    # Initialize ChatGPT handler with API key
    chatgpt = chatgpt_handler.ChatGPT(chatgpt_api_key)

    # Topics the bot will recognize
    conversation_topics = ['precipitation', 'soil moisture']

    # Track conversation status (city, country, topic)
    conversation_status = {
        'city': None,
        'country': None,
        'topic': None,
    }

    # Initial greeting from the bot
    prompt = "You are CliMate, an agri-weather coach. Greet the user and ask how you can help them. (short)"
    response = chatgpt.generate_response(prompt)
    print_response(response)  # Print the greeting

    # Infinite loop to keep conversation ongoing
    while True:
        user_input = get_input()  # Capture user input

        prompt = f"""
            You are a chatbot assisting a user with weather information.
            Here is the user's input: "{user_input}"
            Here is the current conversation status: {conversation_status}
            And here is a list of topics the available: {conversation_topics}.

            Based on this, provide a JSON response with:
            - City
            - Country
            - The topic if the user's input is related to discussion topics if not set to none
            - Ask the user only for the missing conversation statuses
            - Update the conversation status
            - Use 'None' instead of null

            Format the response in JSON like this:
            {{
                "city": "<city>",
                "country": "<country>",
                "topic": "<topic>",
                "message": "<message for user>"
            }}
            """
            
        response = chatgpt.generate_response(prompt)
        response = json.loads(response.strip())
        conversation_status = response

        # Check for missing information in the response
        missing = [key for key in response.keys() if response[key] == 'None']

        # If no information is missing, proceed with fetching weather data
        if len(missing) == 0:
            # Fetch latitude and longitude based on city and country
            lat, lon = JSON_response.get_lat_lon(response['city'], response['country'])

            # Use the EnvironmentLoader instance to call the API
            json_data = env_loader.call_meteomatics_api(lat, lon)

            # Extract precipitation values from the response
            values = [date_entry['value'] for item in json_data['data'] for coordinate in item['coordinates'] for date_entry in coordinate['dates']]

            # Determine flood risk based on precipitation values
            if sum(values) / len(values) < 2:
                print("\nCliMate: Based on the precipitation data gathered from your location, the risk of flooding is low, which creates favorable conditions for farming.\nYou can proceed with confidence, as the current weather patterns support a stable environment for agricultural activities.")
            else:
                print("\nCliMate: Based on the precipitation data gathered from your location, the risk of flooding is high, which creates unfavorable conditions for farming.\nExercise caution, as the current weather patterns indicate potential disruptions to agricultural activities.")
        else:
            print_response(response['message'])

if __name__ == "__main__":
    main()

