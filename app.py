from flask import Flask, request, jsonify
from datetime import date
import model

app = Flask(__name__)

m = model.Model()

@app.route('/', methods=['GET'])
def index():
    return "<center><h2>You've reached stock prediction API home. Please use <br><code><span style='color:red;'> /predict?symbol={symbol}&period={period} </span></code> <br> to get the prediction.</h2></center>"

@app.route('/predict', methods=['GET'])
def predict():
    symbol = request.args.get('symbol')
    period = int(request.args.get('period'))

    TODAY = date.today().strftime("%Y-%m-%d")
    data = m.load_data(symbol, TODAY)
    if(data.empty):
        return jsonify([])
    
    df_train = m.train(data)
    forecast = m.predict(df_train, period)
    forecast_list = forecast_list = [[x[0].strftime('%Y-%m-%d'), x[1]] for x in forecast.values.tolist()]
    # print(forecast_list)
    return jsonify(forecast_list)

if __name__ == '__main__':
    app.run(debug=True)
