import time
import pandas as pd
import os
import string as str
import numpy as np
import sys

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def getRuntime(someFunction):

    def timer(*args, **kwargs):

        t1 = time.time()
        out = someFunction(*args, **kwargs)
        t2 = time.time()
        hours, rem = divmod(t2-t1, 3600)
        minutes, seconds = divmod(rem, 60)
        print('This took {:02.0f}:{:02.0f}:{:05.2f}'.format(hours, minutes, seconds))
        print('-' * 40)

        return out

    return timer


def filter_df(df, month, day):
    """
    Filters the dataframe based on previous user input
    """

    #filter by month
    df = df.loc[df['month'] == month]

    #filter by day
    df = df.loc[df['day_of_week'] == day]

    return df


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter desired city (new york city, chicago, washington): ').lower()

        if city in CITY_DATA:
            break

        print('invalid input, try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter desired month (january : june): ').lower()

        if month in months:
            month = months.index(month) + 1
            break

        print('invalid input, try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter desired day of the week: ').lower()

        if day in days:
            day = days.index(day)
            break

        print('invalid input, try again.')

    print('-' * 40)
    return city, month, day


@getRuntime
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

    print('\nLoading Data...\n')

    path = os.getcwd().replace('\\', '/') + '/'
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
    try:
        df = pd.read_csv(dir_path + CITY_DATA.get(city))
    except FileNotFoundError as e:
        sys.exit('Error loading file. Make sure that the datafiles are in the working directory.\npath: {}\ndir_path: {}'.format(path, dir_path))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    if df is None:
        sys.exit('Error initializing dataframe. File was loaded successfully but load_data() failed.')

    return df


@getRuntime
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating Time Stats...\n')

    # display the most common month
    mode_month = df['month'].mode()[0]
    print('(Pre-filter) the most common month is {}'.format(months[mode_month-1]))

    # display the most common day of week
    mode_day = df['day_of_week'].mode()[0]
    print('(Pre-filter) the most common day is {}'.format(days[mode_day]))

    # apply filter
    df = filter_df(df, month, day)

    # display the most common start hour
    mode_hour = df['day_of_week'].mode()[0]
    print('the most common hour is {}'.format(mode_hour))

    return df


@getRuntime
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating Station Stats...\n')

    # display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    print('the most common start station is {}'.format(mode_start_station))
    
    # display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    print('the most common end station is {}'.format(mode_end_station))
    
    # display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + ',' + df['End Station']
    mode_start_end = list(df['Start End'].mode()[0].split(','))
    print('the most common start and end station combination is {} and {}'.format(mode_start_end[0], mode_start_end[1]))

    return


@getRuntime
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Duration Stats...\n')

    # display total travel time
    total_time = df['Trip Duration'].sum()
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print('The total travel time was {:02.0f}:{:02.0f}:{:05.2f}'.format(hours, minutes, seconds))
    
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    hours, rem = divmod(mean_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print('The mean travel time was {:02.0f}:{:02.0f}:{:05.2f}'.format(hours, minutes, seconds))

    return


@getRuntime
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    if 'User Type' in df.columns:
        value_counts = df['User Type'].value_counts()
        print('The user counts are as follows:')
        for i, v in value_counts.iteritems():
            print(i, ': ', v)
          
    # Display counts of gender
    if 'Gender' in df.columns:
        value_counts = df['Gender'].value_counts()
        print('The user counts are as follows:')
        for i, v in value_counts.iteritems():
            print(i, ': ', v)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df.dropna(subset=['Birth Year'], inplace=True)
        print('The earliest birth year was {:.0f}'.format(df['Birth Year'].min()))
        print('The most recent birth year was {:.0f}'.format(df['Birth Year'].max()))
        print('The most common birth year was {:.0f}'.format(df['Birth Year'].mode()[0]))


def displaydf(df):
    # variable to track position in df
    i = 0
    while True:
        num = input('How many lines would you like to print out? To proceed, type 0 or none.').lower()
        
        # Break condition
        if num == '0' or num == 'none':
            break
        else:
            try:
                num = int(num)
                print(df[i:i+num].to_string() + '\n')
                i += num
            except Exception as e:
                print('Invalid input. Try again')
        
    return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        df = time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        displaydf(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
