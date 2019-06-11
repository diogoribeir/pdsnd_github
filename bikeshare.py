import time
import pandas as pd
import numpy as np
"""
Support for the Project

LIBRARY

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html


STACK OVERFLOW

https://stackoverflow.com/questions/45310254/fixed-digits-after-decimal-with-f-strings

https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary-in-python

https://stackoverflow.com/questions/35523635/extract-values-in-pandas-value-counts/35523820
"""

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


    while True:
        city = input('Which city you want to analyze?\n Chicago, New York City or Washington\n').lower()
        if city.lower() not in ('chicago', 'new york city','washington'):
            print('Choose a avaliable city')
            continue
        else:
            break


    while True:
        month = input('Which month?\n all, january, february, march, april, may or june\n').lower()
        if month.lower() not in ('all','january', 'february', 'march', 'april', 'may','june'):
            print('Choose a existing option')
            continue
        else:
            break



    while True:
        day = input('Which day of the week? \n all, sunday, monday, tuesday, wednesday, thursday, friday or saturday\n').lower()
        if day.lower() not in ('all','sunday', 'monday', 'tuesday',
                                 'wednesday', 'thursday', 'friday','saturday'):
            print('Choose a existing option')
            continue
        else:
            break


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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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

    common_month = df['month'].value_counts().keys()[0]
    print(f'Common month: {common_month}')

    common_day = df['day_of_week'].value_counts().keys()[0]
    print(f'Common day of week: {common_day}')

    hour = df['Start Time'].value_counts().keys()[0]
    hour_only = str(hour)[11:13]
    print(f'Common hour: {hour_only}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start = df['Start Station'].value_counts().keys()[0]
    count_start = df['Start Station'].value_counts().tolist()[0]

    print(f'The most common Start Station is {pop_start} with count: {count_start}')

    pop_end = df['End Station'].value_counts().keys()[0]
    count_end = df['End Station'].value_counts().tolist()[0]
    
    print(f'The most common End Station is {pop_end} with count: {count_end}')
    
    df['Combination Station'] = df['Start Station'] + ' ' + df['End Station']
    pop_combination = df['Combination Station'].value_counts().keys()[0]
    count_combination = df['Combination Station'].value_counts().tolist()[0]

    print(f'The most frequent combination is {pop_combination} with count: {count_combination}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    seconds = df['Trip Duration'].sum()
    minutes = seconds / 60
    hours = minutes / 60
    print(f' Total travel time is:\n seconds:{seconds:.0f}, minutes:{minutes:.0f} and hours is {hours:.0f}')
    
    seconds = df['Trip Duration'].mean()
    minutes = seconds / 60
    hours = minutes / 60
    print(f' Mean travel time is:\n seconds:{seconds:.0f}, minutes:{minutes:.0f} and hours is {hours:.0f}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    users = df['User Type'].value_counts().keys()
    count_users = df['User Type'].value_counts().tolist()
    users_count = dict(zip(users,count_users))
    print(users_count)
"""
Because the washington database does not have the 
Birth Year and Gender columns, it has been included condition for not breaking the code
"""
    if 'Gender' in df.columns:
    
        genders = df['Gender'].value_counts().keys()
        count_genders = df['Gender'].value_counts().tolist()
        genders_count = dict(zip(genders,count_genders))
        print(genders_count)
    else:
        print('\nColumn Gender does not exist in dataset')


    if 'Birth Year' in df.columns:
        earlist,recent,common = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().keys()[0]
        print(f'Earlist: {earlist}, Recent: {recent} and Common: {common}')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('\nColumn Birth Year does not exist in dataset')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        count = 0
        lines = 0

"""        
The loop below shows 5 rows of the dataset, whenever the answer is 'yes'       
"""
        while True:
            
            view = input('You would like to view the 5 lines of the dataset? Enter yes or no.\n').lower()
            
            if view == 'yes':
                print(df.iloc[count:lines+5])
                lines += 5
                count += 5
               
            elif view == 'no':
                break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
