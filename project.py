import time
import pandas as pd
import numpy as np


def maybe_exit(value_typed):
    """Exit the program if the value_typed is 'exit'"""
    if value_typed.lower() == 'exit':
        print("Exiting the program. Have a nice day!")
        exit()

def prompt_allowed_value(values_list, str_detail):
    """Prompts user a value from 'values_list' and return it (or exit if user wants to)"""

    str_values = ', '.join(values_list)
    print(f'Please, write down the {str_detail} ({values_list}) to show the data, or if you want to see data from all of them, type "all"')
    input_prompt = f"Please, type the {str_detail} ({str_values} or 'all'): "
    allowed_values = values_list
    allowed_values.append('All')
    value = False 

    while not value :
        #prompts value and remove spaces in beggining and and, also Capitalize Words
        value = input(input_prompt).title().strip()
        maybe_exit(value)

        if value not in allowed_values:
            print(f"The value you've entered '{value}' is invalid.")
            value = False 
    print(f"Ok. You choose: {value}.\n")
    return value 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('To exit, enter "exit" in any time')

    # gettin user input for city
    city = prompt_allowed_value(["Chicago", "New York City", "Washington"], 'city name')
    # get user input for month (all, january, february, ... , june)
    month = prompt_allowed_value(['January', 'February', 'March', 'April', 'May', 'June'], 'month')
    # get user input for weekday (monday, tuesday, ... , sunday)
    day = prompt_allowed_value(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'week day')

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

    if city.title() == 'All': 
        df_chicago = pd.read_csv('chicago.csv')
        df_new_york = pd.read_csv('new_york_city.csv')
        df_washington = pd.read_csv('washington.csv')
        df = pd.concat([df_chicago, df_new_york, df_washington])
    else:
        filename = city.replace(' ', '_').lower() + '.csv'
        df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    if month.title() != 'All':
        df = df[(df['Start Time'].dt.month_name() == month) | (df['End Time'].dt.month_name() == month)]

    if day.title() != 'All':
        df = df[(df['Start Time'].dt.day_name() == day) | (df['End Time'].dt.day_name() == day)]

    return df

def display_most_common(df, series_names, str_detail):
    if len(series_names) > 1:
        top_value = df.groupby(series_names).size().idxmax()
    else:
        value = df[series_names[0]]
        top_value = value.value_counts().idxmax()
    print(f"The most used {str_detail} is '{top_value}'")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    display_most_common(df, ['Month'], 'month')
    display_most_common(df, ['Day of Week'], 'day of week')
    display_most_common(df, ['Start Hour'], 'start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    display_most_common(df, ['Start Station'], 'start station')
    display_most_common(df, ['End Station'], 'end station')
    display_most_common(df, ['Start Station', 'End Station'], 'trip')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def display_count_values(df, column_name, str_details, type_name):
    count_types = df[column_name].value_counts()
    types = count_types.index
    padding_target_type = len(max(types, key=len)) + 3
    padding_target_value = len(str(max(count_types.tolist())))
    print(f"The types and count of {str_details} are: ")
    print(type_name.rjust(padding_target_type)+ "|" + "total".ljust(padding_target_value))
    print("-".rjust(padding_target_type, '-') + "|" + "|".rjust(padding_target_value+1, '-'))

    for type_values, total_values in count_types.items():
        print(f"{type_values.rjust(padding_target_type)}|{str(total_values).ljust(padding_target_value)}|")
    
    print('')

def display_value(value, str_detail):
    print(f"The {str_detail} is: {value}")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print(f"The total time of the trips is {total_time/86400} days")
    # display mean travel time
    average_duration = df['Trip Duration'].mean()
    print(f"The average duration of the trips is {total_time/60} minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    display_count_values(df, 'User Type', 'users','user type')
    if 'Gender' in df:
        display_count_values(df, 'Gender', 'gender', 'gender')
    else:
        print('There is no information of Users Gender in this dataset.')

    if 'Birth Year' in df:
        year_counted = df['Birth Year'].value_counts()
        earliest = year_counted.index.min()
        most_recent = year_counted.index.max()
        common = year_counted.idxmax()
        display_value(int(earliest), 'earliest year of birth')
        display_value(int(most_recent), 'most recent year of birth')
        display_value(int(common), 'most common year of birth')
    else:
        print('There is no Users Birth Year information in this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break


if __name__ == "__main__":
	main()
