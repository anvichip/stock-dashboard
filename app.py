from flask import Flask, render_template, redirect, url_for, request
from get_prediction import generate_stock_page
from stock_data_yfinance import get_stocks
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


# Original code, not working
# @app.route('/predictions', methods=['GET', 'POST'])
# def predictions():
#     if request.method == 'POST':
#         stock_code = request.form['stock_code']
#         prediction_data = generate_stock_page(stock_code)
#         return render_template('stock_dashboard.html', stock_code=stock_code, prediction_data=prediction_data)
#     return render_template('predictions.html')

@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        stock_code = request.form['stock_code']
        stock_data = get_stocks(stock_code, 365)
        prediction_data = generate_stock_page(stock_data)
        return render_template('stock_dashboard.html', stock_code=stock_code, prediction_data=prediction_data)
    return render_template('predictions.html')


@app.route('/stock_prices', methods=['GET', 'POST'])
def stock_prices():
    if request.method == 'POST':
        stock_code = request.form['stock_code']
        stock_data = get_stocks(stock_code, 365)
        return render_template('stock_data.html', tables=[stock_data.to_html(classes='data')], titles=stock_data.columns.values)
    return render_template('stock_prices.html')


@app.route('/news')
def news():
    return render_template('news.html')


if __name__ == '__main__':
    app.run(debug=True)
