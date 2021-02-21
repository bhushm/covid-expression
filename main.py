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
        COUNTRY_ISO_CODE: {
            FREEDOM_PARAMETER: FREEDOM_VALUE,
            ...
        },
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
    """
    Cluster the countries based on their freedom of expression values.

    Returns a list in the following format, where each sublist is a list of countries in a single cluster:

    [
        [
            COUNTRY_ISO_CODE,
            ...
        ],
        ...
    ]
    """

    data = freedom_data()

    # Load the freedom data as a DataFrame, with each row being a single country.
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
    countries = list(data.keys())

    # Initialize the list to hold the clusters, with one sublist for each cluster label
    clusters = []
    for label in sorted(set(labels)):
        clusters.append([])

    # Add the countries one-by-one to the correct sublist
    for i in range(len(countries)):
        country = countries[i]
        label = labels[i]

        clusters[label].append(country)

    return clusters


def freedom_averages():
    """
    Find the freedom of expression superscore for each cluster.

    Returns a list in the following format:

    [
        FREEDOM_SUPERSCORE_AVERAGE,
        ...
    ]
    """

    clusters = country_clusters()
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


def response_averages():
    """
    Find the average COVID response for each cluster at the end of 2020.

    Returns a list in the following format:

    [
        RESPONSE_FINAL_AVERAGE,
        ...
    ]
    """

    clusters = country_clusters()
    averages = []

    for cluster in clusters:
        response_values = []

        with open(RESPONSE_FILENAME) as response_file:
            response_reader = csv.DictReader(response_file)

            for row in response_reader:
                country = row["Code"]
                date = row["Date"]

                if country in cluster and date == "2020-12-31":
                    response_values.append(float(row["stringency_index"]))

        response_average = round(sum(response_values) / len(response_values), 4)
        averages.append(response_average)

    return averages


# Print results for testing
print(
    country_clusters(),
    freedom_averages(),
    response_averages(),
    sep="\n\n",
)
