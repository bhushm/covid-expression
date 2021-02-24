# Import and run functions from scripts here.

from scripts.countries import (
    shared_countries,
)

from scripts.clusters import (
    freedom_data,
    country_clusters,
)

from scripts.averages import (
    freedom_averages,
    final_response_averages,
    seasonal_response_averages,
)

from scripts.plots import (
    final_response_plot
)


countries = shared_countries()

freedom_data = freedom_data(countries)
clusters = country_clusters(freedom_data)

print(
    freedom_averages(clusters),
    final_response_averages(clusters),
    seasonal_response_averages(clusters),
    final_response_plot(clusters),
    sep="\n",
)
