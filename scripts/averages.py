import csv
import datetime

from . import FREEDOM_FILENAME, RESPONSE_FILENAME


def freedom_averages(clusters):
    """
    Find the freedom of expression superscore for each cluster.

    Accepts a list of lists, with each sublist containing a list of country ISO codes (see country_clusters()).

    Returns a list in the following format:

    [
        FREEDOM_SUPERSCORE_AVERAGE,
        ...
    ]
    """

    averages = []

    for cluster in clusters:
        freedom_values = []

        with open(FREEDOM_FILENAME) as freedom_file:
            freedom_reader = csv.DictReader(freedom_file)

            for row in freedom_reader:
                # Only use the rows from 2017 (see README).
                if row["year"] == "2017":
                    country = row["ISO_code"]

                    if country in cluster:
                        freedom_values.append(float(row["pf_expression"]))

        freedom_average = round(sum(freedom_values) / len(freedom_values), 4)
        averages.append(freedom_average)

    return averages


def final_response_averages(clusters):
    """
    Find the average COVID response for each cluster at the end of 2020.

    Accepts a list of lists, with each sublist containing a list of country ISO codes (see country_clusters()).

    Returns a list in the following format:

    [
        FINAL_RESPONSE_AVERAGE,
        ...
    ]
    """

    averages = []

    for cluster in clusters:
        response_values = []

        with open(RESPONSE_FILENAME) as response_file:
            response_reader = csv.DictReader(response_file)

            for row in response_reader:
                country = row["Code"]
                date = row["Date"]

                if (country in cluster) and (date == "2020-12-31"):
                    response_values.append(float(row["stringency_index"]))

        averages.append(round(sum(response_values) / len(response_values), 4))

    return averages


def seasonal_response_averages(clusters):
    """
    Find the average COVID response for each cluster for each season of 2020.

    Accepts a list of lists, with each sublist containing a list of country ISO codes (see country_clusters()).

    Returns a list in the following format (each sublist is for a single cluster):

    [
        [
            SPRING_RESPONSE_AVERAGE,
            SUMMER_RESPONSE_AVERAGE,
            FALL_RESPONSE_AVERAGE,
        ],
        ...
    ]
    """

    seasonal_averages = []

    # The dates being used across the project for seasons
    SPRING_START = datetime.date(2020, 4, 1)
    SUMMER_START = datetime.date(2020, 6, 1)
    FALL_START = datetime.date(2020, 9, 1)
    END = datetime.date(2020, 12, 1)

    for cluster in clusters:
        spring_response_values = []
        summer_response_values = []
        fall_response_values = []

        with open(RESPONSE_FILENAME) as response_file:
            response_reader = csv.DictReader(response_file)

            for row in response_reader:
                country = row["Code"]
                date = row["Date"]

                if country in cluster:
                    # Convert the date to a datetime object for comparison
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

                    if SPRING_START <= date < SUMMER_START:
                        spring_response_values.append(float(row["stringency_index"]))

                    if SUMMER_START <= date < FALL_START:
                        summer_response_values.append(float(row["stringency_index"]))

                    if FALL_START <= date < END:
                        fall_response_values.append(float(row["stringency_index"]))

        seasonal_averages.append(
            [
                round(sum(spring_response_values) / len(spring_response_values), 4),
                round(sum(summer_response_values) / len(summer_response_values), 4),
                round(sum(fall_response_values) / len(fall_response_values), 4),
            ]
        )

    return seasonal_averages
