import csv


FREEDOM_FILENAME = "data/human-freedom-index-2019.csv"
RESPONSE_FILENAME = "data/covid-stringency-index.csv"


def shared_countries():
    """
    Find all countries that are shared between the freedom and response datasets (by ISO code).

    Returns a list in the following format:

    [COUNTRY_ISO_CODE, ...]
    """

    # The countries (by ISO code) that are in the two datasets.
    freedom_countries = []
    response_countries = []

    with open(FREEDOM_FILENAME) as freedom_file:
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:
            # Only use the rows from 2017 (see README).
            if row["year"] == "2017":
                country = row["ISO_code"]

                if not country in freedom_countries:
                    freedom_countries.append(country)

    with open(RESPONSE_FILENAME) as response_file:
        response_reader = csv.DictReader(response_file)

        for row in response_reader:
            country = row["Code"]

            if not country in response_countries:
                response_countries.append(country)

    freedom_countries = set(freedom_countries)
    response_countries = set(response_countries)

    shared_countries = sorted(freedom_countries & response_countries)

    return shared_countries


def freedom_data():
    """
    Find the freedom of expression data for the countries.

    Returns a dictionary in the following format:

    {
        COUNTRY_NAME: LIST_OF_VALUES,
        ...
    }
    """

    countries = shared_countries()

    # The columns in the freedom of expression dataset that will be used.
    freedom_columns = [
        "pf_expression_killed",
        "pf_expression_jailed",
        "pf_expression_influence",
        "pf_expression_control",
        "pf_expression_cable",
        "pf_expression_newspapers",
        "pf_expression_internet",
    ]

    freedom_data = {}

    with open(FREEDOM_FILENAME) as freedom_file:
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:
            # Check if the row has the right year and country values
            if row["year"] == "2017" and row["ISO_code"] in countries:
                country = row["ISO_code"]

                try:
                    freedom_data[country] = [
                        float(row[column]) for column in freedom_columns
                    ]

                # Skip the country if any of the values were blank or otherwise could not be converted to a number.
                except ValueError:
                    continue

    return freedom_data


def country_clusters():
    """Cluster the countries based on their freedom of expression values."""
