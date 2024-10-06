# Michelin Guide Restaurants Dashboard

Dashboard for analyzing Michelin Guide Restaurants (part of the Plotly Dash [Autumn App Challenge 2024](https://community.plotly.com/t/autumn-app-challenge/87373)).

Some of the visualizations available:

* **Geographical Distribution**: A map showing the location of Michelin-starred restaurants.
* **Awards Distribution**: Breakdown of distribution of Michelin rating (also per country).
* **Cuisine Popularity**: Count of restaurants by cuisine type.
* **Price Range Distribution**: Number of restaurants in each price range.
* **Green Stars**: Distribution of restaurants that have earned the Green Star.
* **Top Locations**: Cities with the most Michelin-starred restaurants.
* **Top Countries**: Countries with the most Michelin-starred restaurants.

## Getting started

### Installation
To set up the project, ensure you have Python 3.11+ installed. Follow these steps:

Clone the repository:

```shell
git clone https://github.com/niekvleeuwen/michelin-guide-restaurants-dashboard.git
cd michelin-guide-restaurants-dashboard
```

Ensure poetry is available, e.g. on Ubuntu/Debian you can run the following:

```shell
apt-get install python3 poetry
```

Install dependencies using Poetry:

```shell
poetry install
```

Then enter the created virtual environment:

```shell
poetry shell
```

Next, install the pre-commit hooks
```shell
pre-commit install
```

The program can be executed using:

```shell
python dashboard/main.py
```
