import boto3
import csv
import os
import random
import datetime
# Testing pipeline 1
def create_temp_files(bucket, key):
    file_extension = key.split('.')[-1]
    
    if file_extension == 'csv':
        s3_client = boto3.client('s3')
        s3_object = s3_client.get_object(Bucket=bucket, Key=key)
        
        csv_content = s3_object['Body'].read().decode('utf-8')

        # Create a temporary file path
        temp_input_file = f"/tmp/{key}"
        temp_output_file = temp_input_file.replace('.csv', '_output.csv')
        
        # Write the original CSV content to the temporary input file
        with open(temp_input_file, 'w', newline='') as input_file:
            input_file.write(csv_content)
        
        return temp_input_file, temp_output_file
    else:
        print(f"File type not supported")
        return None, None

def write_to_bucket(bucket, temp_output_file):
    s3_client = boto3.client('s3')

    # Upload the output file to the S3 bucket as the name of the file in /tmp
    with open(temp_output_file, 'rb') as data:
        s3_client.put_object(
            Bucket=bucket, 
            Key=os.path.basename(temp_output_file),
            Body=data
        )

def select_data(file_path, num_points):
    """Reads data and performs some validation on it"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                datetime.datetime.strptime(row[1], "%d-%m-%Y")
            except ValueError:
                print(f"Invalid date format in row: {row}")
                return None
            try:
                float(row[2])
            except ValueError:
                print(f"Invalid number in row: {row}")
                return None
            data.append(row)
    
    if len(data) >= num_points:
        start_index = random.randint(0, len(data) - num_points)
        return data[start_index:start_index + num_points]
    else:
        print("Not enough data points available.")
        return None

def predict_data_LSEG(data, data_points_number):
    prices = [float(row[2]) for row in data]
    
    def recursive_predict(prices, n, result):
        if n == 1:
            result.append(sorted(prices)[-2])
        elif n == 2:
            result.append(sorted(prices)[-2] + (prices[-1] - sorted(prices)[-2]) / 2)
        else:
            prev = result[-1]
            ante_prev = result[-2]
            next_value = prev + (prev - ante_prev) / 2**(n-1)
            result.append(next_value)

    def predict_data_recursive(prices, num_predictions):
        result = []
        recursive_predict(prices, 1, result)
        recursive_predict(prices, 2, result)
        for i in range(3, num_predictions + 1):
            recursive_predict(prices, i, result)
        return result

    predicted_prices = predict_data_recursive(prices, data_points_number)

    last_date_str = data[-1][1]
    last_date = datetime.datetime.strptime(last_date_str, "%d-%m-%Y")
    stock_id = data[-1][0]

    predicted_data = []
    for index, price in enumerate(predicted_prices):
        predicted_date = last_date + datetime.timedelta(days=index+1)
        predicted_date_str = predicted_date.strftime("%d-%m-%Y")
        predicted_data.append([stock_id, predicted_date_str, price])
    
    return predicted_data

def lambda_handler(event, context):
    for record in event['Records']:
        object_key = record['s3']['object']['key']

    current_region = os.environ['AWS_REGION']

    bucket_name = f"project-stocks-vxmm-{current_region}"
    output_bucket = f"output-stocks-vxmm-{current_region}"

    temp_input_file, temp_output_file = create_temp_files(bucket_name, object_key)
    
    if temp_input_file and temp_output_file:
        data = select_data(temp_input_file, 10)
        
        if data:
            predicted_prices = predict_data_LSEG(data, 3)
            
            with open(temp_output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(predicted_prices)
            
            write_to_bucket(output_bucket, temp_output_file)
            
            # Clean up the temporary files
            os.remove(temp_input_file)
            os.remove(temp_output_file)

if __name__ == '__main__':
    lambda_handler(None, None)
