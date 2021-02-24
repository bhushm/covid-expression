import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from . import (
    FREEDOM_FILENAME,
    RESPONSE_FILENAME,
    SPRING_START,
    SUMMER_START,
    FALL_START,
    WINTER_START,
    END,
)


def final_response_plot(clusters):
    """
    Generate a plot for the final response values versus freedom of expression.

    Accepts a list of lists, with each sublist containing a list of country ISO codes (see country_clusters()).
    """

    x_values = []
    y_values = []

    # Use list comprehension to get a simple list of countries from cluster sublists
    countries = [country for cluster in clusters for country in cluster]

    with open(FREEDOM_FILENAME) as freedom_file:
        freedom_reader = csv.DictReader(freedom_file)

        for row in freedom_reader:
            # Only use the rows from 2017 (see README).
            if row["year"] == "2017":
                country = row["ISO_code"]

                if country in countries:
                    x_values.append(float(row["pf_expression"]))

        with open(RESPONSE_FILENAME) as response_file:
            response_reader = csv.DictReader(response_file)

            for row in response_reader:
                country = row["Code"]
                date = row["Date"]

                if (country in countries) and (date == "2020-12-31"):
                    y_values.append(float(row["stringency_index"]))

    linear_regression = LinearRegression()

    x_values_reshaped = [[element] for element in x_values]
    y_values_reshaped = [[element] for element in y_values]
    linear_regression.fit(x_values_reshaped, y_values_reshaped)

    # mx + b
    x = np.linspace(0, 10, 1000)
    m = linear_regression.coef_[0][0]
    b = linear_regression.intercept_[0]

    plt.plot(x, m * x + b)
    plt.scatter(x_values, y_values)

    plt.grid(True)
    plt.axis([0, 10, 0, 100])

    plt.suptitle("COVID Response Stringency vs. Freedom of Expression (12/31/2020)")
    plt.title("Linear Regression: y = " + str(round(m, 2)) + "x + " + str(round(b, 2)), pad=10)

    plt.xlabel("Freedom of Expression Index")
    plt.ylabel("COVID Response Stringency Index")

    path = "results/images/final.png"

    plt.savefig(path, dpi=150)

    return path
