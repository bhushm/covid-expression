import csv

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
            if row['year'] == '2017': # Only use the rows from 2017
                iso_code = row["ISO_code"] # The ISO Code of the country

                if not iso_code in freedom_countries:
                    freedom_countries.append(iso_code) # Add the ISO Code to the list

    with open(RESPONSE_FILENAME) as response_file:

        # Read the COVID response file
        response_reader = csv.DictReader(response_file)

        for row in response_reader:
            iso_code = row["Code"] # The ISO Code of the country
            if not iso_code in response_countries:
                response_countries.append(iso_code) # Add the ISO Code to the list

    freedom_countries = set(freedom_countries)
    response_countries = set(response_countries)

    # Return all of the shared country codes
    return sorted(freedom_countries & response_countries)


def cluster_countries():
    """Cluster the countries using k-means by freedom of expression."""

    # All of the countries to be used
    countries = find_shared_countries()

    # The expression data for the countries
    expression_data = {}

    with open(FREEDOM_FILENAME) as freedom_file:

        # The names of the expression column names in the CSV file
        expression_column_names = [
            "pf_expression_killed",
            "pf_expression_jailed",
            "pf_expression_influence",
            "pf_expression_control",
            "pf_expression_cable",
            "pf_expression_newspapers",
            "pf_expression_internet",
        ]

        # Read the human freedoms file
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:

            # Check if the row has the right year and country values
            if row["year"] == "2017" and row["ISO_code"] in countries:

                # The country ISO code
                country = row["ISO_code"]

                # The expression data for the country
                expression_data[country] = {}

                # Add the data for each desired column
                for column_name in expression_column_names:

                    # Get the column value (and return None if it is not a number)
                    try:
                        value = float(row[column_name])
                    except ValueError:
                        value = None

                    expression_data[country][column_name] = value
