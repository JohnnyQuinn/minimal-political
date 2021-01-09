import requests

from flask import Flask, request, render_template
from pprint import PrettyPrinter

app = Flask(__name__)

pp = PrettyPrinter(indent=1)

@app.route("/")
def homepage():
    senate_members_url = "https://api.propublica.org/congress/v1/116/senate/members.json"
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(senate_members_url, headers=headers).json()

    senate_members_list = r["results"][0]["members"]

    print("---------------------------------------------------------")

    return render_template('home.html')

@app.route("/lawmaker-results")
def lawmaker_results():
    context = {
        'lawmaker_name': request.args.get('lawmaker-query')
    }
    return render_template('lawmaker-results.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
