# sqlalchemy-challenge

Step 1 - Climate Analysis and Exploration
To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

Precipitation Analysis

1. Start by finding the most recent date in the data set.
2. Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.
3. Select only the date and prcp values.
4. Load the query results into a Pandas DataFrame and set the index to the date column.
5. Sort the DataFrame values by date.
6. Plot the results using the DataFrame plot method.
7. Use Pandas to print the summary statistics for the precipitation data.

Station Analysis

1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most active stations (i.e. which stations have the most rows?).
3. List the stations and observation counts in descending order.
4. Which station id has the highest number of observations?
5. Using the most active station id, calculate the lowest, highest, and average temperature.
6. Design a query to retrieve the last 12 months of temperature observation data (TOBS).
7. Filter by the station with the highest number of observations.
8. Query the last 12 months of temperature observation data for this station.
9. Plot the results as a histogram with bins=12.
10. Close out your session.

Step 2 - Climate App

1. Use Flask to create your routes.
2. List all routes that are available.
    /api/v1.0/precipitation
    Convert the query results to a dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary.

    /api/v1.0/stations
    Return a JSON list of stations from the dataset.
    /api/v1.0/tobs
    Query the dates and temperature observations of the most active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year.

    /api/v1.0/<start> and /api/v1.0/<start>/<end>
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date. 
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
  
Bonus: Other Recommended Analyses

Temperature Analysis I
1. Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?
2. Use pandas to perform this portion.
3. Convert the date column format from string to datetime.
4. Set the date column as the DataFrame index
5. Drop the date column
6. Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.
7. Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?
