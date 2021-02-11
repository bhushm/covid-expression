import csv

FREEDOM_FILENAME = "human-freedom-index-2019.csv"
RESPONSE_FILENAME = "covid-stringency-index.csv"


def shared_countries():
    """Find all countries that are shared between the datasets (by ISO Code)."""

    # The countries (by ISO Code) that are shared between the datasets.
    shared_countries = []

    # The countries (by ISO Code) that are in the freedom dataset.
    freedom_countries = []

    # The countries (by ISO code) that are the in response dataset.
    response_countries = []

    with open(FREEDOM_FILENAME) as freedom_file:
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:
            if row['year'] == '2017': # Only use the rows from 2017.
                iso_code = row["ISO_code"] # The ISO Code of the country

                if not iso_code in freedom_countries:
                    freedom_countries.append(iso_code) # Add the ISO Code to the list

    with open(RESPONSE_FILENAME) as response_file:
        response_reader = csv.DictReader(response_file)

        for row in response_reader:
            iso_code = row["Code"] # The ISO Code of the country
            if not iso_code in response_countries:
                response_countries.append(iso_code) # Add the ISO Code to the list

    freedom_countries = set(freedom_countries)
    response_countries = set(response_countries)

    # Return all of the shared country codes
    return sorted(freedom_countries & response_countries)


print(shared_countries())
