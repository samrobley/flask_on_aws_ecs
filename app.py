from flask import Flask, render_template, request, jsonify

import database

dynamodb = None

def connect():
    database.create_table()
    return database.connect_table()

app = Flask(__name__)

app.route("/demo")
def demo():
    # return templates/demo/bootstrap_demo.html
    return render_template('demo/bootstrap_demo.html')

@app.route("/", methods=['GET', 'POST'])
def index():
    global dynamodb
    if request.method == 'POST':
        print(request.form)
        #database.add_record()
        return render_template('index.html')

    if request.method == 'GET':
        # Query DynamoDB and retrieve data
        dynamodb = connect()
        table_name = 'todo_list'
        print(f'Querying table {table_name} for all records')
        
        response = dynamodb.scan(TableName=table_name)
        
        print(f'Response from dynamodb: {response}')

        items = response.get('Items', [])
        # Create a list to store the data to pass to the template
        data_to_pass = []

        # response.get shape is:
        # {'Items': [{'list_id': '1', 'item_id': 'item-1', 'item_data': 'New Item', 'item_order': Decimal('1')}, {'list_id': '1', 'item_id': 'item-2', 'item_data': '+ Add Item', 'item_order': Decimal('2')}, {'list_id': '1', 'item_id': 'item-3', 'item_data': 'Save Order', 'item_order': Decimal('3')}], 'Count': 3, 'ScannedCount': 3, 'ResponseMetadata': {'RequestId': 'cf3087b7-2388-4943-a8f0-37d234f3301b', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Sat, 21 Oct 2023 22:19:18 GMT', 'x-amzn-requestid': 'cf3087b7-2388-4943-a8f0-37d234f3301b', 'content-type': 'application/x-amz-json-1.0', 'x-amz-crc32': '1253999157', 'content-length': '339', 'server': 'Jetty(11.0.11)'}, 'RetryAttempts': 0}}

        # Loop through the items and add them to the data_to_pass list

        for item in items:
            print(item)
            
            list_id = None
            item_id = item['item_id']
            item_order = str(item['item_order'])

            # get item_data from this item {'list_id': '1', 'item_id': 'item-6', 'item_data': 'Save Order', 'item_order': Decimal('6')}
            item_data = str(item['item_data'])
            print(f'Item data is: {item_data}')
            data_to_pass.append([list_id, item_id, item_data, item_order])

        print(f'Data to pass is: {data_to_pass}')

        return render_template('index.html', data=data_to_pass)

@app.route("/save-order", methods=['POST'])
def save_order():
    # Get the data from the request
    # print it to console
    data = request.get_json()
    print("printing data")
    print(data)
    response = {'message': 'Order saved successfully'}
    print("printing data finished")

    # example data: [{'id': 'item-1', 'text': 'New Item'}, {'id': 'item-2', 'text': 'New Item'}, {'id': 'item-3', 'text': 'New Item stuff'}, {'id': 'item-4', 'text': '+ Add Item'}, {'id': 'item-5', 'text': 'Save Order'}]

    # save this data to dynamodb using a foreach and the database.add_record(table,data) function
    
    for item in data:
        print(item)
        database.add_record(dynamodb, item)


    return jsonify(response)

if __name__ == "__main__":
    # you need host='0.0.0.0' to run on docker container
    app.run(debug=True, host='0.0.0.0')

