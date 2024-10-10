import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key='AIzaSyBT4qz_pSZrB8yCqfQeU7jm1YhQYumhDQw')


def persona(input):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(input)

    return response.text


# Title of the app
st.title("Travel Personality Quiz")

# Introduction
st.write("""
    Welcome to the Travel Personality Quiz! 
    This quiz is designed to help you discover your travel personality based on your interests, lifestyle, and preferences.
""")

# Category 1: Interests and Lifestyle
st.header("Category 1: Interests and Lifestyle")
entertainment_options = ["Music", "Sports", "Movies", "Games", "Art", "Live Concerts", "Books", "Festivals"]
entertainment = st.multiselect("Select your favorite entertainment:", entertainment_options)

comfort_options = ["Luxury", "Premium", "Comfort", "Economy", "Budget"]
comfort = st.multiselect("Select your comfort level:", comfort_options)

# Category 2: Places and Seasons
st.header("Category 2: Places and Seasons")
favorite_place_options = ["City", "Beach", "Rural", "Mountain"]
favorite_place = st.multiselect("Select your favorite place:", favorite_place_options)

planning_style_options = ["Meticulous", "Flexible", "Spontaneous"]
planning_style = st.multiselect("Select your planning style:", planning_style_options)

top_season_options = ["Weekends", "Holidays", "Mid Season", "Off-peak", "Occasions"]
top_season = st.multiselect("Select your top season:", top_season_options)

travel_frequency_options = ["Zero", "One - Two", "Three - Five", "Six - Nine", "10+ Times"]
travel_frequency = st.multiselect("How often do you travel?", travel_frequency_options)

# Category 3: My Trip
st.header("Category 3: My Trip")
trip_type_options = ["Adventure", "Events", "Touristic", "Business",
                     "Immersive", "Nature", "Relaxation",
                     "Wellness", "Romantic", "Cultural"]
trip_type = st.multiselect("Select your trip type:", trip_type_options)

tribe_options = ["Solo", "Couple", "Family", "Friends", "Groups", "Pet"]
tribe = st.multiselect("Who do you travel with?", tribe_options)

travel_activities_options = ["Hiking/Walking", "Sight Seeing",
                             "Zip lining", "Shopping",
                             "Food", "Cycling",
                             "Cruises", "Horseriding",
                             "Kayaking", "Ice Skating",
                             "Dance"]
travel_activities = st.multiselect("Select your favorite travel activities:", travel_activities_options)

# Submit button
if st.button("Submit"):
    # Compile results into a prompt for the persona function
    user_input = f"""
        You are an AI assistant for a travel application that assigns a personality to each user based on their interests. 
        The interests are divided into the following categories:

        Category 1: Interests and Lifestyle.
        Sub category (a) - Entertainment: {', '.join(entertainment)}
        Sub category (b) - Your Comfort: {', '.join(comfort)}

        Category 2: Places and Seasons.
        Sub category (a) - Favorite place: {', '.join(favorite_place)}
        Sub category (b) - Planning style: {', '.join(planning_style)}
        Sub category (c) - Top Season: {', '.join(top_season)}
        Sub category (d) - Travel frequency: {', '.join(travel_frequency)}

        Category 3: My Trip.
        Sub category (a) - Trip Type: {', '.join(trip_type)}
        Sub category (b) - Tribe: {', '.join(tribe)}
        Sub category (c) - Travel Activities: {', '.join(travel_activities)}

        What type of personality does a traveler with these interests have? 
        The traveler type can only be one of the following options:
        Adventurer, City Slickers, Culture Chasers, Unwinder, Nature Buff, Centric, Homebody, Sightseeing, Offbeater, Foodee, Shopper. 
        If the user's persona does not fit into any of these categories, simply output null. 
        Also if a user has some traits of another persona, give a probability of the strength of each persona from 0 to 1.
    """

    # Get personality prediction from the model
    personality_result = persona(user_input)

    # Display results
    st.header("Your Travel Personality Results!")

    # Show user selections
    for key, value in {
        'Interests': entertainment,
        'Comfort Level': comfort,
        'Favorite Place': favorite_place,
        'Planning Style': planning_style,
        'Top Season': top_season,
        'Travel Frequency': travel_frequency,
        'Trip Type': trip_type,
        'Travel Tribe': tribe,
        'Travel Activities': travel_activities
    }.items():
        st.write(f"{key}: {', '.join(value) if value else 'None selected'}")

    # Show personality predictions
    st.subheader("Personality Prediction:")
    st.write(personality_result)
