import csv
from pandas import DataFrame
from sklearn.cluster import KMeans


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

    shared_countries = sorted(list(freedom_countries & response_countries))

    return shared_countries


def freedom_data():
    """
    Find the freedom of expression data for the countries.

    Returns a dictionary in the following format:

    {
        COUNTRY_ISO_CODE: LIST_OF_VALUES,
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

                # Initalize a dictionary to store the freedom data for the country
                freedom_data[country] = {}

                try:
                    for column in freedom_columns:
                        freedom_data[country][column] = float(row[column])

                # Skip the country if any of the values were blank or otherwise could not be converted to a number.
                except ValueError:
                    # Delete the country from the data
                    del freedom_data[country]

                    continue

    return freedom_data


def country_clusters():
    """Cluster the countries based on their freedom of expression values."""

    data = freedom_data()

    # Load the freedom data as a DataFrame, with each row being a single country.
    keys = list(data.keys())
    data_array = DataFrame.from_dict(data, orient="index")

    kmeans = KMeans(
        n_clusters=4,
        n_init=15,
        max_iter=300,
        tol=0.0001,
    )

    # Cluster the countries by freedom of expression data.
    kmeans.fit(data_array)

    labels = kmeans.labels_

    clusters = {}
    for label in sorted(set(labels)):
        clusters[label] = []

    for i in range(len(keys)):
        country = keys[i]
        label = labels[i]

        clusters[label].append(country)

    return clusters


def response_averages():
    """Find the COVID response averages for each cluster of countries."""

    clusters = country_clusters()

    for cluster_number in clusters:
        cluster = clusters[cluster_number]

        # The countries (by ISO code) that are in the two datasets.
        freedom_values = []
        response_values = []

        with open(FREEDOM_FILENAME) as freedom_file:
            freedom_reader = csv.DictReader(freedom_file)

            for row in freedom_reader:
                # Only use the rows from 2017 (see README).
                if row["year"] == "2017":
                    country = row["ISO_code"]

                    if country in cluster:
                        freedom_values.append(float(row["pf_expression"]))

        with open(RESPONSE_FILENAME) as response_file:
            response_reader = csv.DictReader(response_file)

            for row in response_reader:
                country = row["Code"]
                date = row["Date"]

                if country in cluster and date == "2020-12-31":
                    response_values.append(float(row["stringency_index"]))

        print(
            cluster_number,
            "average expression score:",
            round(sum(freedom_values) / len(freedom_values), 4),
            "average response score:",
            round(sum(response_values) / len(response_values), 4),
        )


response_averages()
