# flask --app data_server run
from flask import Flask
from flask import render_template
import json
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    filename = os.path.join(app.root_path, 'data', 'life_expectancy.json')

    with open(filename) as test_file:
        data = json.load(test_file)

    polylines = []
    labels_y_vals = []

    avg_sum = 0
    avg_count = 0
    for country in ["Canada", "Mexico", "United States"]:

        polyline = []

        for year in range(1960, 2021):
            out = []
            out.append(str(50 + (year-1960)*6.66))
            out.append(str(450-4*(data[country][str(year)])))

            avg_sum += data[country][str(year)]
            avg_count += 1
            print(out)
            polyline.append(out)
            if year == 2020:
                labels_y_vals.append(out[1])
        
        for i in range(len(polyline)):
            polyline[i] = ",".join(polyline[i])
        polyline = " ".join(polyline)
        print("--")
        print(polyline)
        print("--")
        polylines.append(polyline)

        avg = avg_sum/avg_count



    return render_template('index.html', polylines = polylines, labels_y_vals = labels_y_vals, data = data, avg = avg)

@app.route('/year')
def year():
    return render_template('year.html')

app.run(debug=True)
