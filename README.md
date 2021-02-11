# Freedom of the Press vs. COVID Response

## Introduction

This project focuses on how freedom of the press in a particular country compares to the *strictness* of the country's COVID response.

(*Strictness* is not the same as *effectiveness*, this project focuses **only** on *strictness*)

## Data

- `human-freedom-index-2019.csv`
    - This project measures freedom of the press using data from the Human Freedom Index 2019 (https://www.cato.org/human-freedom-index/2019).
        - The report from *2019* is used, but it only contains data up to 2017. This is because (as explained on the HFI website), 2017 is the most recent year that sufficient data was available to create the report (the 2018 report included data up to 2016, the 2017 report included data up to 2015, and so on).
        - Only data from 2017 (the most recent) is used.
- `covid-stringency-index.csv`
    - This project measures stringency of COVID response using data from Our World In Data (https://ourworldindata.org/covid-government-stringency-index)
        - Although this data includes data up to the current day (in 2021), only data for *2020* is used.

## Development

- Create the virtual environment and install the required packages (python 3.6+).
    ```
    python -m venv venv
    python -m pip install -r requirements.txt
    ```

## Methods

- This project uses k-means clustering to cluster the countries into groups based on their freedom of press levels.
- The COVID response stringency levels are then compared between these clusters.
