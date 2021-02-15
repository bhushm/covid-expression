import os
import csv
import matplotlib.pyplot as plt


FREEDOM_FILENAME = "data/human-freedom-index-2019.csv"
RESPONSE_FILENAME = "data/covid-stringency-index.csv"


def find_shared_countries():
    """Find all countries that are shared between the datasets (by ISO Code)."""

    # The countries (by ISO Code) that are in the freedom dataset.
    freedom_countries = []

    # The countries (by ISO code) that are the in response dataset.
    response_countries = []

    with open(FREEDOM_FILENAME) as freedom_file:

        # Read the human freedoms file
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:
            if row["year"] == "2017":  # Only use the rows from 2017
                iso_code = row["ISO_code"]  # The ISO Code of the country

                if not iso_code in freedom_countries:
                    freedom_countries.append(iso_code)  # Add the ISO Code to the list

    with open(RESPONSE_FILENAME) as response_file:

        # Read the COVID response file
        response_reader = csv.DictReader(response_file)

        for row in response_reader:
            iso_code = row["Code"]  # The ISO Code of the country
            if not iso_code in response_countries:
                response_countries.append(iso_code)  # Add the ISO Code to the list

    freedom_countries = set(freedom_countries)
    response_countries = set(response_countries)

    # Return a list all of the shared country codes
    return sorted(freedom_countries & response_countries)


# def compare_response_freedom():
#     """Simple example function that compares the COVID response and freedom of expression of the countries."""
#
#     countries = find_shared_countries()
#
#     countries_data = {}
#     for country in countries:
#         countries_data[country] = {}
#
#     with open(FREEDOM_FILENAME) as freedom_file:
#         freedom_reader = csv.DictReader(freedom_file)
#
#         for row in freedom_reader:
#             if row['year'] == '2017':
#                 iso_code = row["ISO_code"]
#
#                 if iso_code in countries:
#                     countries_data[iso_code]['freedom'] = row['pf_expression']
#
#     with open(RESPONSE_FILENAME) as response_file:
#         response_reader = csv.DictReader(response_file)
#
#         for row in response_reader:
#             iso_code = row["Code"]
#
#             if iso_code in countries:
#                 countries_data[iso_code]['response'] = row['stringency_index']
#
#     raw_countries_data = [(float(pair['freedom']), float(pair['response'])) for pair in list(countries_data.values())]
#
#     plt.scatter(*zip(*raw_countries_data))
#
#     plt.savefig('results/compare.png')
#
# compare_response_freedom()
