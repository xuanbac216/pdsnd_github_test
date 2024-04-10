import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = ''
    while True:
        city = input('Enter the city name. (Example: /New York City/Chicago/Washington): ')
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print('The City name is invalid, please check it again')

    # get user input for month (all, january, february, ... , june)
    month = ''
    MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Please enter the month (Example: All/January/February/.../June) : ')
        month = month.lower()
        if month in MONTH_DATA:
            break
        else:
            print('The Month is invalid, please check it again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    DAY_OF_WEEEKS = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Please enter the day of the week (Example: All/Monday/Tuesday/.../Sunday) : ')
        day = day.lower()
        if day in DAY_OF_WEEEKS:
            break
        else:
            print('The Day is invalid, please check it again')

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
    ## Get the file name
    file_name = CITY_DATA[city]
    ## read the input file
    df = pd.read_csv(file_name)
    ## convert the data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    ## filter month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    ## filter by day of week
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month  = df['month'].mode()[0]
    print('\nMost common month:', most_common_month)

    #display the most common day of week
    most_common_day_of_week  = df['day_of_week'].mode()[0]
    print('\nMost common day of week:', most_common_day_of_week)

    #display the most common start hour
    most_common_start_hour  = df['hour'].mode()[0]
    print('\nMost most common start hour:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # The Most Popular Stations and Trip
    most_common_trip  = df.groupby(['Start Station','End Station'])['Start Station'].count().nlargest(1)
    print('\nMost commonly used trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: " + str(round(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: " + str(round(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        count_of_user_types = df['User Type'].value_counts()
        print("\nCount of user types: " + str(count_of_user_types))
    except KeyError:
        print('User Type stats cannot be calculated because User Type does not appear in the dataframe')
    
    # Display counts of gender
    try:
        count_of_gender = df['Gender'].value_counts()
        print("\nCount of gender: " + str(count_of_gender))
    except KeyError:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]

        print("\nEarliest year of birth: " + str(int(earliest_year)))
        print("\nMost common year of birth: " + str(int(most_common_year)))
        print("\nMost recent year of birth: " + str(int(most_recent_year)))
    except KeyError:
        print("\nYear of birth is not exist in this db.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays data"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if view_data.lower() != 'yes':
        return
    
    start_location = 0
    print(df.head())
    while True:
        print(df.iloc[start_location:start_location+5])
        start_location += 5
        view_data = input("Do you want to continue? Enter yes or no.").lower()
        if view_data.lower() != 'yes':
            return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
