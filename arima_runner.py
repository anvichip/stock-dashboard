from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


def arima_train_and_plot(data, col_name, Ntest, p, d, q):
    # split data to train and test sets based on N_test value
    train = data.iloc[:-Ntest]
    test = data.iloc[-Ntest:]
    train_idx = data.index <= train.index[-1]
    test_idx = data.index > train.index[-1]

    # Define and fit the arima model
    arima = ARIMA(train[col_name], order=(p, d, q))
    arima_res = arima.fit()

    # plot the real values of stock prices
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(data[col_name], label='Actual return')

    # plot the fitted values of model (in sample data predicted values)
    train_pred = arima_res.fittedvalues
    ax.plot(train.index, train_pred, color='green', label='fitted')

    # plot the forecast values of model (out of sample data predicted values)
    prediction_res = arima_res.get_forecast(Ntest)
    conf_int = prediction_res.conf_int()
    # lower and upper limits of prediction
    lower, upper = conf_int[conf_int.columns[0]], conf_int[conf_int.columns[1]]
    forecast = prediction_res.predicted_mean
    ax.plot(test.index, forecast, label='forecast')
    ax.fill_between(test.index, lower, upper, color='red', alpha=0.3)
    ax.legend()

    # evaluating the model using RMSE and MAE metrics
    y_true = test[col_name].values
    rmse = np.sqrt(mean_squared_error(y_true, forecast))
    mae = mean_absolute_error(y_true, forecast)

    return arima_res, rmse, mae


def run_this(df):
    arima_res, rmse, mae = arima_train_and_plot(
        df, 'Close', Ntest=30, p=0, d=1, q=0)
    forecast_next_day = arima_res.get_forecast(
        steps=1).predicted_mean.values[0]
    return forecast_next_day
    # print('Root Mean Squared Error: ', rmse)
    # print('Mean Absolute Error: ', mae)
