from flask import Flask, render_template, redirect, url_for, request
from get_prediction import generate_stock_page
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        stock_code = request.form['stock_code']
        prediction_data = generate_stock_page(stock_code)
        return render_template('stock_dashboard.html', prediction_data=prediction_data)
    return render_template('predictions.html')


@app.route('/stock_prices')
def stock_prices():
    return render_template('stock_prices.html')

@app.route('/news')
def news():
    return render_template('news.html')

if __name__ == '__main__':
    app.run(debug=True)
