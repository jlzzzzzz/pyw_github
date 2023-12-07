import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def check_data_entry(prompt, valid_entries): 
    """
    Function that asks the user to input data and verifies if it's valid.
    This simplifies the get_filters() function, where we need to ask the user for three inputs.
    Args:
        (str) prompt - message to show to the user
        (list) valid_entries - list of accepted strings 
    Returns:
        (str) user_input - user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries : 
            print('It looks like your entry is incorrect.')
            print('Let us try again!')
            user_input = str(input(prompt)).lower()

        print('Great! You have chosen: {}\n'.format(user_input))
        return user_input

    except:
        print('There seems to be an issue with your input.')
              
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df
              

              
              
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most Common Month:", most_common_month)

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("Most Common Day of Week:", most_common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station:", most_common_start_station)


    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most Commonly Used End Station:", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    station_combination_counts = df.groupby(['Start Station', 'End Station']).size()
    most_common_station_combination = station_combination_counts.idxmax()
    print("Most Frequent Combination of Start and End Station Trip:", most_common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()/ 3600.0 
    print("Total travel time:", total_travel_time, "hours")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/ 60.0 
    print("Mean travel time:", mean_travel_time, "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("No gender data available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", most_recent_year)
        print("Most Common Year of Birth:", most_common_year)
    else:
        print("No birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays Raw data."""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(df):
            print("No more data to display.")
            break
        view_data = input("Do you wish to continue viewing more data? Enter yes or no: ").lower()
   

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
      
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')     
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
