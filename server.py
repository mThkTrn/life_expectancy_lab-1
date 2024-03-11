# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
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

            avg_sum += float(out[1])
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

        avg_height = avg_sum/avg_count
        print(f"avg_height = {avg_height}")



    return render_template('index.html', polylines = polylines, labels_y_vals = labels_y_vals, data = data, avg_height = avg_height)

@app.route('/year')
def year():

    filename = os.path.join(app.root_path, 'data', 'life_expectancy.json')

    with open(filename) as test_file:
        data = json.load(test_file)

    requested_year = request.args.get("year")

    expectancies = [data["Canada"][requested_year], data["Mexico"][requested_year], data["United States"][requested_year]]
    last_expecs = [data["Canada"][str(int(requested_year)-1)], data["Mexico"][str(int(requested_year)-1)], data["United States"][str(int(requested_year)-1)]]
    diffs = [expectancies[0] - last_expecs[0], expectancies[1] - last_expecs[1], expectancies[2] - last_expecs[2]]
    qualsum = []
    for diff in diffs:
        if diff == 0:
            qualsum.append("the same as the last year")
        elif diff > 0:
            qualsum.append("increased from the last year")
        elif diff < 0:
            qualsum.append("decreased from the last year")

    def expectancyToColor(expectancy):
        return f"({round(255-((expectancy-50) * (255/50)))},{round(255-((expectancy-50) * (255/50)))}, 255)"
    
    colors = [expectancyToColor(j) for j in expectancies]

    colorstr = ";".join(colors)
    print(colors, colorstr)
    expectancies = [round(expectancy) for expectancy in expectancies]
    legendvals  = [expectancyToColor(age for age in range(50, 110, 10))]
    print(legendvals)
    return render_template('year.html', year = requested_year, colors = colors, colorstr = colorstr, expectancies = expectancies, qualsum = qualsum)

app.run(debug=True)
