""" An application that interacts with the API Ninjas Exercise API to generate a personalised workout plan for the user, with optional motivational quotes through using API Ninjas Quotes API """

import requests
# The requests library is used for making HTTP requests in Python - used for the APIs
from pprint import pprint as pp
# The pprint module in Python is a utility module that is used to print data structures in a more readable way
import random
# random module used in this program to randomise quotes returned with Quotes API
import os
# the os module provides a way of using operating system dependent functionality like reading or writing to the file system - needed for dotenv
from dotenv import load_dotenv
# the load_dotenv function from the python-dotenv package loads environment variables from a .env file into the environment variables of the operating system.

# for API key:
# ensure the python-dotenv package is installed - run command: pip3 install python-dotenv
# the same API key is used for both APIs
load_dotenv()
# load environment variables from .env file
api_key = os.getenv('API_KEY')
# retrieve the API key from the environment variables


def user_nickname():
    # get user name and slice to create initial nickname
    name = input(
        "Welcome to your motivational workout app! To get a personalised workout, please start by telling us your name: ").strip().upper()
    # strip() removes any leading or tailing whitespace or characters ensuring clean and consistent data
    # upper() converts characters to upper case - ensures that input comparisons and further processing can be performed without issues with case variations
    nickname = name[:1]
    # slice name string to first letter and store to nickname variable
    return nickname


def user_fitness_level(user_nickname):
    # get user fitness level
    fitness_level = input(
        f"It's great to meet you, {user_nickname}, (we like nicknames around here)! To make sure the plan we create is right for you, please tell us your fitness level (beginner, intermediate, expert): ").strip().lower()
    # lower() converts characters to lower case - ensures that input comparisons and further processing can be performed without issues with case variations
    return fitness_level


def get_quotes():
    # get motivational quotes from quotes API
    category = 'fitness'
    quote_API = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(
        category)
    # using the .format() method to dynamically insert the difficulty variable into the API URL. This ensures that the chosen difficulty level by the user is correctly embedded in the API request URL
    quote_response = requests.get(
        quote_API, headers={'X-Api-Key': api_key})
    # Make the API request with the API key
    quotes = quote_response.json()
    # parse exercise data from API so that it is readable in a python format (ie dictionaries)
    return quotes


def get_exercises(user_fitness_level, api_key):
    # get exercises from exercise API based on fitness level
    workout_API = 'https://api.api-ninjas.com/v1/exercises?difficulty={}'.format(
        user_fitness_level)
    exercise_response = requests.get(workout_API, headers={
        'X-Api-Key': api_key})
    # Make the API request for exercise data with the API key
    exercise_data = exercise_response.json()  # returns 10 exercises
    exercises = exercise_data[:5]
    # slice the list to limit the number of exercises in workout plan to the first 5
    return exercises


def create_workout_plan(exercises, quote):
    # function takes a list of exercises and an optional quote as input
    # create workout plan with a motivational quote:
    workout_plan = {
        'quote': {
            'author': quote['author'],
            'text': quote['quote']
        } if quote else None,
        # dictionary used to store data - takes a 'quote' key, which stores the quote author and quote text if a quote is provided, otherwise set to None.
        'exercises': [{'name': exercise['name'], 'muscle': exercise['muscle'], 'equipment': exercise['equipment'], 'difficulty': exercise['difficulty'], 'instructions': exercise['instructions']} for exercise in exercises]
    }
    # dictionary used to store data - takes an 'exercise' key, which stores data retrieved for exercises
    return workout_plan


def save_workout_plan(workout_plan, plan_file, user_nickname):
    # function takes a workout plan dictionary and a file name as inputs
    # write workout plan to a file
    with open(plan_file, 'w') as file:
        # open a file to write / save personalised plan in it
        file.write(
            f"{user_nickname}, below is your personalised plan. We hope you enjoy your workout! \n")
        file.write("\n")
        if workout_plan['quote']:
            file.write(f"""To keep you motivated, here is a quote by {workout_plan['quote']['author']}: {
                       workout_plan['quote']['text']} \n\n""")
        # if a motivational quote is present in the workout plan, it writes the author and quote to the file
        for exercise in workout_plan['exercises']:
            file.write(f"Exercise: {exercise['name']} \n")
            file.write(f"Muscle: {exercise['muscle']} \n")
            file.write(f"Equipment: {exercise['equipment']} \n")
            file.write(f"Difficulty: {exercise['difficulty']} \n")
            file.write(f"Instructions: {exercise['instructions']} \n")
            file.write("\n")
        # iterates over the exercises in the workout plan and writes the details of each exercise to the file
    pp(f"Your motivational workout has been saved to '{plan_file}'")


def main():
    # main function to run full program
    nickname = user_nickname()
    # gets user nickname
    difficulty = user_fitness_level(nickname)
    # gets the user's fitness level
    include_quotes = input(
        "Would you like some extra encouragement with a motivationl quote in your workout plan (y / n)?  ").strip().lower()
    # gets motivational quote if the user wants one
    quotes = get_quotes() if include_quotes == 'y' else None
    # boolean logic used to check if user wants a quote included, if 'y' then Quotes API will fetch a quote
    quote = random.choice(quotes) if quotes else None
    # if the user wants a quote, it fetches motivational quotes and selects one randomly
    exercises = get_exercises(difficulty, api_key)
    # fetches exercises based on the user's fitness level
    workout_plan = create_workout_plan(exercises, quote)
    # creates a workout plan that includes the selected exercises and the motivational quote
    save_workout_plan(workout_plan, 'workout_plan.txt', nickname)


main()
