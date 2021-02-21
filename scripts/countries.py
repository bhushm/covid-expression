import csv

from . import FREEDOM_FILENAME, RESPONSE_FILENAME


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
