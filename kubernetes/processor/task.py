from flask import Flask, request, send_file
import csv
import random
import datetime
import io

app = Flask(__name__)

def select_data(file, num_points):
    """Reads data and performs some validation on it"""
    data = []
    reader = csv.reader(file)
    for row in reader:
        try:
            datetime.datetime.strptime(row[1], "%d-%m-%Y")
        except ValueError:
            return "ERROR: Incorrect date format. Expected dd-mm-yyyy.", None
        try:
            float(row[2])
        except ValueError:
            return "ERROR: Invalid number in third column.", None
        data.append(row)

    if len(data) >= num_points:
        start_index = random.randint(0, len(data) - num_points)
        return None, data[start_index:start_index + num_points]
    else:
        return "ERROR: Insufficient data points.", None

def predict_data(data, data_points_number):
    """Generate predicted data based on input data"""
    prices = [float(row[2]) for row in data]
    predicted_prices = []
    
    for i in range(1, data_points_number + 1):
        if i == 1:
            predicted_prices.append(sorted(prices)[-2])
        elif i == 2:
            predicted_prices.append(sorted(prices)[-2] + (prices[-1] - sorted(prices)[-2]) / 2)
        else:
            prev = predicted_prices[-1]
            ante_prev = predicted_prices[-2]
            next_value = prev + (prev - ante_prev) / 2**(i-1)
            predicted_prices.append(next_value)
    
    last_date_str = data[-1][1]
    last_date = datetime.datetime.strptime(last_date_str, "%d-%m-%Y")
    stock_id = data[-1][0]
    
    predicted_data = []
    for index, price in enumerate(predicted_prices):
        predicted_date = last_date + datetime.timedelta(days=index + 1)
        predicted_date_str = predicted_date.strftime("%d-%m-%Y")
        predicted_data.append([stock_id, predicted_date_str, price])
    
    return predicted_data

@app.route("/process", methods=["POST"])
def process_csv():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    
    selected_data = select_data(file, 10)
    predicted_data = predict_data(selected_data, 3)
    
    # Create in-memory CSV file
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(predicted_data)
    output.seek(0)
    
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')), 
                     mimetype="text/csv", 
                     as_attachment=True, 
                     download_name="predicted_data.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)