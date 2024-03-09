from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show  # Assuming you're using show


app = Flask(__name__)


def create_plot(data):
    """Creates a Bokeh histogram of the 'rate_paid_to_carrier_dollars' column in a DataFrame.

    Args:
        data: pandas DataFrame containing trip data.

    Returns:
        str: HTML representation of the Bokeh plot.
    """
    # Ensure data is a DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")

    # Check if 'rate_paid_to_carrier_dollars' column exists
    if 'rate_paid_to_carrier_dollars' not in data.columns:
        raise ValueError("Input DataFrame must contain a column named 'rate_paid_to_carrier_dollars'")

    # Create a Bokeh figure object
    p = figure(title="Distribution of Rate Paid to Carrier",
               x_axis_label="Rate Paid to Carrier (Dollars)",
               y_axis_label="Frequency")

    def create_hist_data(col_name, num_bins=10):
        t_val, t_bin = np.histogram(data[col_name], bins=num_bins)
        return pd.DataFrame(data={'count': t_val, col_name: (t_bin[:-1] + t_bin[1:]) / 2}), t_bin[1] - t_bin[0]

    t_data, t_bin_size = create_hist_data("rate_paid_to_carrier_dollars")
    p.vbar(x="rate_paid_to_carrier_dollars", top="count", width=t_bin_size, source=t_data, legend_label="Rate Distribution")
    del t_data, t_bin_size

    # Convert Bokeh plot object to HTML representation
    return show(p, return_unused=True)  # Get HTML without rendering


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        user_input = request.form["user_input"]
        df = pd.read_csv('synthetic_data_set.csv')

        # Generate plot (optional)
        plot_data = create_plot(df)

        return render_template("index.html", message=f"You entered: {user_input}", data_available=True,
                               plot_data=plot_data)
    else:
        return render_template("index.html", message="", data_available=False)


if __name__ == "__main__":
    app.run(debug=True)
