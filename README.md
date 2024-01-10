# Stock Price Forecasting

This is a simple Flask web application for a stock dashboard. The application includes pages for home, predictions, stock prices, and news. Users can input stock codes to get predictions and view stock prices.
1. Developed a financial solution which uses LSTM+ARIMA to predict stock price, works for long and short term sight.
2. Used live data to predict trends, using yfinance.
3. Added a functionality where the sentimental analysis of stock's news affects how the model deals with it, webscraped live using beautifulSoup.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Functionalities](#functionalities)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/anvichip/stock-dashboard.git
    ```

2. Navigate to the project directory:

    ```bash
    cd stock-dashboard
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to [http://localhost:5000/](http://localhost:5000/) to access the stock dashboard.

## Project Structure

- `app.py`: Main Flask application file.
- `templates/`: HTML templates for the different pages.
- `static/`: Static files such as CSS stylesheets and images.
- `requirements.txt`: List of Python dependencies.
- `scripts`: Helper methods for the application.

## Dependencies

- Flask
- mplfinance (for generating financial charts)
- pandas
- beautifulsoup4
- numpy
- transformers
- pandas_ta
- yfinance
- mpmath
- networkx
- sympy
- torch
- sentencepiece
- huggingface-hub

## Functionalities

### Home

The home page provides a welcoming message and acts as the starting point for the application.

### Predictions

1. **Enter stock code for analysis:**
   - Users can input a stock code and click the "Submit" button to get predictions for the specified stock. The application uses a function to generate prediction data and displays it on the Stock Dashboard page.

### Stock Prices

1. **Enter stock code for stock prices:**
   - Users can input a stock code and click the "Submit" button to get historical stock prices for the specified stock. The application uses a function to generate stock data in the form of a DataFrame and displays it on the Stock Data page.

### News

1. **Latest Stock News:**
   - Clicking the "News" button on the navigation bar takes users to the latest stock news page.

2. **Generate Summary:**
   - Users can click on a news article to generate a summary for that specific article.


