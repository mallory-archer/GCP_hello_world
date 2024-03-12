from flask import Flask, render_template, request
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)


def create_plot(data):
    """Creates a Matplotlib histogram of the 'rate_paid_to_carrier_dollars' column in a DataFrame.

    Args:
        data: pandas DataFrame containing trip data.

    Returns:
        tuple: (image, data_available): BytesIO object containing the plot image and a boolean indicating data availability.
    """

    # Ensure data is a DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")

    # Check if 'rate_paid_to_carrier_dollars' column exists
    if not all(col in data.columns for col in ['rate_paid_to_carrier_dollars', 'rate_type']):
        raise ValueError("Input DataFrame must contain columns named 'rate_paid_to_carrier_dollars' and 'rate_type'")

        # Use Agg backend for headless generation
    matplotlib.use('Agg')
    plt.style.use(os.path.join('static', 'plot_styles.mplstyle'))

    # Create a Matplotlib figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Histogram
    # ax.hist(data["rate_paid_to_carrier_dollars"], bins=10)
    # ax.set_title("Distribution of Rate Paid to Carrier")
    # ax.set_xlabel("Rate Paid to Carrier (Dollars)")
    # ax.set_ylabel("Frequency")

    # Generate box plots for different rate types
    data.boxplot(column="rate_paid_to_carrier_dollars", by="rate_type", ax=ax1)
    ax1.set_title("Rate Paid to Carrier Distribution by Rate Type")
    ax1.set_xlabel("Rate Type")
    ax1.set_ylabel("Rate Paid to Carrier (Dollars)")

    # Calculate daily average rate paid to carrier by rate type
    daily_rates = data.groupby(['load_date', 'rate_type'])['rate_paid_to_carrier_dollars'].mean().unstack()

    # Timeseries plot for average rate paid to carrier colored by rate type
    daily_rates.plot(kind='line', ax=ax2)
    ax2.set_title("Average Rate Paid to Carrier by Load Date and Rate Type")
    ax2.set_xlabel("Load Date")
    ax2.set_ylabel("Average Rate Paid to Carrier (Dollars)")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability with dates

    # Convert plot to PNG image
    img_io = BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)

    # Close the figure
    plt.close(fig)

    return img_io.getvalue()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        user_input = request.form["user_input"]
        df = pd.read_csv('synthetic_data_set.csv')

        # Generate plot
        plot_data = create_plot(df)

        # Encode plot data as base64
        plot_image = base64.b64encode(plot_data).decode('utf-8')

        return render_template("index.html", message=f"You entered: {user_input}", data_available=True,
                               plot_image=plot_image)
    else:
        return render_template("index.html", message="", data_available=False)


if __name__ == "__main__":
    app.run(debug=True)
