from flask import Flask, render_template, request
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
    if 'rate_paid_to_carrier_dollars' not in data.columns:
        raise ValueError("Input DataFrame must contain a column named 'rate_paid_to_carrier_dollars'")

    # Use Agg backend for headless generation
    matplotlib.use('Agg')

    # Create a Matplotlib figure
    fig, ax = plt.subplots()
    ax.hist(data["rate_paid_to_carrier_dollars"], bins=10)
    ax.set_title("Distribution of Rate Paid to Carrier")
    ax.set_xlabel("Rate Paid to Carrier (Dollars)")
    ax.set_ylabel("Frequency")

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
