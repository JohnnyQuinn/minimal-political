import requests
import jinja2

from flask import Flask, request, render_template
from pprint import PrettyPrinter

app = Flask(__name__)

pp = PrettyPrinter(indent=1)

@app.route("/")
def homepage():
    senate_members_url = "https://api.propublica.org/congress/v1/116/senate/members.json"
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(senate_members_url, headers=headers).json()

    senate_members_data = r["results"][0]["members"]

    house_members_url = "https://api.propublica.org/congress/v1/116/house/members.json"

    r = requests.get(house_members_url, headers=headers).json()

    house_members_data = r["results"][0]["members"]

    full_congress_list = create_members_list(senate_members_data, house_members_data)

    context = {
        'full_congress_list': full_congress_list,
    }

    return render_template('home.html', **context)

def create_members_list(member_data1, member_data2):
    member_list = []
    for member in member_data1:
        fullname = {
            'first_name': member['first_name'],
            'last_name': member['last_name']
        }
        member_list.append(fullname)
    for member in member_data2:
        fullname = {
            'first_name': member['first_name'],
            'last_name': member['last_name']
        }
        member_list.append(fullname)

    return member_list

@app.route("/lawmaker-results")
def lawmaker_results():
    lawmaker_query = requests.get.args('lawmaker-query')

    context = {
        'lawmaker_name': request.args.get('lawmaker-query')
    }
    return render_template('lawmaker-results.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
