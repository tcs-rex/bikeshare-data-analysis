import time
import pandas as pd
import numpy as np

# city options for user input
CITY_DATA = { 'CHI': 'chicago.csv',
              'NYC': 'new_york_city.csv',
              'WSH': 'washington.csv' }

# months and days options for user input
months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE']
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('-'*12, ' Program Start ', '-'*12)

    print('\nHello! Let\'s explore some US bikeshare data!')

    while True:

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('\nPlease choose city (enter "CHI" for Chicago, "NYC" for New York City, "WSH" for Washington, or "q" to quit the program): ').upper()

        while city != 'Q':
            if (city == 'CHI' or city == 'NYC' or city == 'WSH'):
                break
            else:
                print('\nSorry, "{}" is an invalid entry. '.format(city))
                city = input('\nPlease enter a valid city id (CHI, NYC, or WSH) or enter "q" to quit: ').upper()

        # If user did not choose to quit...get user input for month (all, january, february, ... , june)
        if city == 'Q':
            month = 'Q'
            day = 'Q'
        else:
            month = input('\nPlease choose month (all, January, February, ... , June) or "q" to quit program: ').upper()

            while month != 'Q':
                if (month == 'ALL' or month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH' or month == 'APRIL' or month == 'MAY' or month == 'JUNE'):
                    break
                else:
                    print('\nSorry, "{}" is an invalid entry. '.format(month))
                    month = input('\nPlease enter a valid month (January to June inclusive) or enter "q" to quit: ').upper()

        # If user did not quit, get user input for day of week (all, monday, tuesday, ... sunday)
        if month == 'Q':
            day = 'Q'
        else:
            day = input('\nPlease choose day of interest (all, Monday, Tuesday, ..., Sunday) or "q" to quit program\n: ').upper()

            while day != 'Q':
                if (day == 'ALL' or day == 'MONDAY' or day == 'TUESDAY' or day == 'WEDNESDAY' or day == 'THURSDAY' or day == 'FRIDAY' or day == 'SATURDAY' or day == 'SUNDAY'):
                    break
                else:
                    print('\nSorry, "{}" is an invalid entry. '.format(day))
                    day = input('\nPlease enter a valid month (January to June inclusive) or enter "q" to quit\n: ').upper()

        # display user inputs to be used for analysis or re-enter inputs
        if (month != 'Q' and day != 'Q'):
            print('-'*7, ' User Inputs Specified ', '-'*7)
            print('\nCity: ', city, '\nMonth (or ALL): ', month, '\nDay (or ALL): ', day, '\n')
            g2g = input('\nEnter "y" to proceed with these inputs, or enter any other key to choose new inputs: \n').lower()
            if g2g == 'y':
                print('Statistics will print below...','\n')
                time.sleep(2)
                return city, month, day
        else:
            print('\nProgram Quit Successfully.\n')
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

    #Create full city dataframe with new columns to allow filtering
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    # df month filter
    if month != 'ALL':
        df = df[df['Month'] == months.index(month) + 1]

    # df day filter
    if day != 'ALL':
        df = df[df['Day'] == days.index(day)]

    return df


def time_stats(df, city, month, day):
    """
    Displays statistics on the most common times of travel.
        4 filter options are coded in this function:
            1 - Specific Month + All days
            2 - Specific Month + Specific day
            3 - All Months + Specific day
            4 - All Months + All days (i.e. no date filters)
    """

    print('-'*12, ' Time Stats ', '-'*13)

    # day and hour stats for specific mth
    if (month != 'ALL' and day == 'ALL'):
        print('\nCalculating Most Common Travel Times for Month Specified ({})...\n'.format(month).title())
        start_time = time.time()

        # display the most common day(s) of week for mth
        print('Most common day(s) of travel:')
        day_mode = df['Day'].mode()
        for mode in day_mode:
            print(days[mode])

        # display the most common start hour(s) for mth
        freq_hr = df['Hour'].mode().to_string(index=False)
        print('Most common hour(s) of travel:\n', freq_hr)

    # Most common hour(s) for specified month and day
    elif (month != 'ALL' and day != 'ALL'):
        print('\nCalculating Most Common Hour to Travel for Specified Month ({}) and Day ({})...\n'.format(month, day).title())
        start_time = time.time()

        # display the most common start hour for specified mth & day
        freq_hr = df['Hour'].mode().to_string(index=False)
        print('Most common hour(s) of travel:\n', freq_hr)

    # Most common month(s) and hour(s) for specified day
    elif (month == 'ALL' and day != 'ALL'):
        print('\nCalculating Most Common Travel Times associated with Specified Day ({})...\n'.format(day).title())
        start_time = time.time()

        # display the most common mth(s) of travel
        print('Most common month(s) of travel:\n')
        mth_mode = df['Month'].mode()
        for mode in mth_mode:
            print(months[(mode - 1)])
        print('\n')

        # display the most common hour(s) of travel
        freq_hr = df['Hour'].mode().to_string(index=False)
        print('Most common hour(s) of travel:\n', freq_hr)

    # else: display 'ALL', ie. most common mth(s), day(s), hr(s) based on entire city dataframe
    else:
        print('\nCalculating Most Common Travel Times for ({})...\n'.format(city))
        start_time = time.time()

        print('Most common month(s) of travel:')
        mth_mode = df['Month'].mode()
        for mode in mth_mode:
            print(months[(mode - 1)])

        print('Most common day(s) of travel:')
        day_mode = df['Day'].mode()
        for mode in day_mode:
            print(days[mode])

        freq_hr = df['Hour'].mode().to_string(index=False)
        print('Most common hour(s) of travel:\n', freq_hr)

    print("\nThis took %s seconds." % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n')
    print('-'*12, ' Station Stats ', '-'*12)

    print('\nCalculating The Most Popular Stations and Trip(s) Based on User Inputs...\n')
    start_time = time.time()

    # display most commonly used start station(s)
    freq_start_station = df['Start Station'].mode().to_string(index=False)
    print('Most common trip Start Station(s):', '\n', freq_start_station, '\n')

    # display most commonly used end station(s)
    freq_end_station = df['End Station'].mode().to_string(index=False)
    print('Most common trip End Station(s):', '\n', freq_end_station, '\n')

    # display most frequent combination(s) of start station and end station trip
    # creates new column from both and the Start and End Stations, then gets mode()
    df['trip_stations'] = df['Start Station'] + ' / ' + df['End Station']
    freq_trip = df['trip_stations'].mode().to_string(index=False)
    print('Most common Start and End Station Combination(s):', '\n', freq_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n')
    print('-'*9, ' Trip Duration Stats ', '-'*10)

    print('\nCalculating Trip Duration Stats Based on User Inputs...\n')
    start_time = time.time()

    # Total (i.e. sum of) travel time for trips in specified dataframe
    sum_duration = round((df['Trip Duration'].sum() / 3600 / 24), 1)
    print('Total sum of trip travel/rental times:\n', sum_duration, ' days')

    # Max trip travel time for trips in specified dataframe
    max_duration = round(df['Trip Duration'].max() / 3600, 1)
    print('Max trip/rental duration:\n', max_duration, ' hours')

    # Min trip travel time for trips in specified dataframe
    min_duration = round(df['Trip Duration'].min() / 60, 1)
    print('Min trip/rental duration:\n', min_duration, ' mins')

    # Mean travel time for trips in specified dataframe
    mean_duration = round(df['Trip Duration'].mean() / 60, 1)
    print('Mean trip/rental duration:\n', mean_duration, ' mins')

    print("\nThis took %s seconds." % (time.time() - start_time))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n')
    print('-'*14, ' User Stats ', '-'*14)

    print('\nCalculating User Stats Based on User Inputs...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of Users by Type:\n', df['User Type'].value_counts().to_string(), '\n')

    # Checks if gender and birth year columns exist 1st, then provides stats if available
    if 'Gender' in df.columns:
        # Display counts of gender
        print('Number of Users by Gender:\n', df['Gender'].value_counts().to_string(), '\n')
    else:
        print('Gender Data Not Available for Specified City', '\n')
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('User Birth Year Stats:')
        print('Youngest:\n', int(df['Birth Year'].max()))
        print('Oldest:\n', int(df['Birth Year'].min()))
        print('Average:\n', int(round(df['Birth Year'].mean(),0)), '\n')
    else:
        print('Birth Year Data Not Available for Specified City', '\n')

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40, '\n')


def r_data(df, city, month, day):
    """
    r_data: Shows raw data for specified dataframe.

    Sliding 5-row window accomplished via iloc and While Loop with window
    start and end variable incrementations.
    """

    print('-'*14, '  Raw Data  ', '-'*14, '\n')
    pd.set_option('display.max_columns', None)

    # if user didnt previously apply filters, the filtered raw data view is not available.
    if month == 'ALL' and day == 'ALL':
        print('Available raw data viewing options:')
        print('  "c" - unfiltered, full City dataset')
        print('  Enter any other key to skip\n')

        print('For reference, your filters are:')
        print('City: {}, Month: {}, Day: {}'.format(city, month, day))
        print('\n')

        opt = input('Enter raw data view option:\n',)
        print('\n')

        # proceed with unfiltered city dataset
        if opt.lower() == 'c':
            win_start = 0
            win_end = 5
            while True:
                start_time = time.time()
                print(df.iloc[win_start: win_end])
                print('\n')
                print("This took %s seconds." % (time.time() - start_time))
                print('-'*40, '\n')
                more = input('To view additional data, enter "y", enter any other key to stop raw data viewing:\n',)
                if more.lower() == 'y':
                    win_start += 5
                    win_end += 5
                else:
                    print('-'*40, '\n')
                    break

    # else if user applied month & day filters previously..2 options available
    else:
        print('Available raw data viewing options:')
        print('  "f" - filtered data based on your previous inputs')
        print('  "c" - full City dataset (removes month and day filters)')
        print('  Enter any other key to skip\n')

        print('For reference, your filters are:')
        print('City: {}, Month: {}, Day: {}'.format(city, month, day))
        print('\n')

        opt = input('Enter raw data view option:\n',)

        # proceed with filtered dataset (note gaps in row index)
        if opt.lower() == 'f':
            start_time = time.time()
            win_start = 0
            win_end = 5
            while True:
                print(df.iloc[win_start: win_end])
                print('\n')
                print("This took %s seconds." % (time.time() - start_time))
                print('-'*40, '\n')
                more = input('To view additional data, enter "y", enter any other key to stop raw data viewing:\n',)
                if more.lower() == 'y':
                    win_start += 5
                    win_end += 5
                else:
                    print('-'*40)
                    break

        # proceed with full city dataset, removes month and day filters
        elif opt.lower() == 'c':
            start_time = time.time()
            full_df = pd.read_csv(CITY_DATA[city])
            win_start = 0
            win_end = 5
            while True:
                print(full_df.iloc[win_start: win_end])
                print('\n')
                print("This took %s seconds." % (time.time() - start_time))
                print('-'*40, '\n')
                more = input('To view additional data, enter "y", enter any other key to stop raw data viewing:\n',)
                if more.lower() == 'y':
                    win_start += 5
                    win_end += 5
                else:
                    print('-'*40)
                    break


def ds_stats(city):
    """ds_stats: Shows general city dataset info/statistics"""
    print('-'*12, '  Dataset Info  ', '-'*12, '\n')
    start_time = time.time()

    # load full city dataset
    full_df = pd.read_csv(CITY_DATA[city])

    # display general info for DataFrame
    print('General dataset info/stats:\n')
    print(full_df.info(),'\n')
    print(full_df.describe(),'\n')

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40, '\n')


def main():
    """Main function: calls functions, checks user inputs, passes inputs/args"""
    while True:
        city, month, day = get_filters()

        # checks if user wanted to quit/exit the program
        if (city == 'Q' or month == 'Q' or day == 'Q'):
            break
        else:
            df = load_data(city, month, day)

        #Once confirmed that user wants to proceed, and data is loaded main() calls sub functions
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # checks if user would like to see raw data for full city dataset or based on user filters
        r_stats_input = input('Do you want to view RAW DATA? If yes, enter "y", otherwise enter any other key to skip:\n', )
        if r_stats_input.lower() == 'y':
            print('\n')
            r_data(df, city, month, day)
        else:
            print('-'*40, '\n')

        # checks if user would like to see summary stats for the city dataset
        city_ds_stats = input('To view DATASET INFO for the full city dataset, enter "y". Enter any other key to skip.\n', )
        if city_ds_stats.lower() == 'y':
            print('\n')
            ds_stats(city)
        else:
            print('-'*40, '\n')

        # checks if user would like to see summary stats for the city dataset
        restart = input('If you would you like to restart the program, enter "y". Enter any other key to quit.\n')
        if restart.lower() != 'y':
            print('-'*40, '\n')
            print('Program Quit Successfully.\n')
            break
        else:
            continue

if __name__ == "__main__":
	main()
