from flask import Flask, request, json

app = Flask(__name__)

house_appliance = {"android_tv": "50000", "refrigerator": "28000", "washing_machine": "39000", "ac": "31000",
                   "microwave": "12000"}


@app.route('/data', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return house_appliance
    if request.method == 'POST':
        data = request.json
        house_appliance.update(data)
        return 'data got inserted'


@app.route("/data/<id>", methods=['PUT'])
def update(id):
    data = request.form['item']
    house_appliance[str(id)] = data
    return 'data updated'


@app.route("/data/<id>", methods=["DELETE"])
def delete_Operation(id):
    house_appliance.pop(str(id))
    return 'data deleted'


if __name__ == '__main__':
    app.run(debug=True)