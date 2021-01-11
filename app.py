import requests
import jinja2

from flask import Flask, request, render_template
from pprint import PrettyPrinter

app = Flask(__name__)

pp = PrettyPrinter(indent=1)

@app.route("/")
def homepage():

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

def get_lawmaker_info(name):
    """ takes in user inputted name of a lawmaker and returns the lawmaker's info (full name, chamber, id, party)"""
    senate_members_url = "https://api.propublica.org/congress/v1/116/senate/members.json"
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(senate_members_url, headers=headers).json()

    senate_members_data = r["results"][0]["members"]

    house_members_url = "https://api.propublica.org/congress/v1/116/house/members.json"

    r = requests.get(house_members_url, headers=headers).json()

    house_members_data = r["results"][0]["members"]

    lawmaker_info = {
        'name': '',
        'id': '',
        'chamber': '',
        'party': ''
    }
    name = name.lower()

    for member in house_members_data:
        lawmaker_full_name = f'{member["first_name"]} {member["last_name"]}'
        if name in lawmaker_full_name.lower():
            lawmaker_info['name'] = lawmaker_full_name
            lawmaker_info['id'] = member['id']
            lawmaker_info['chamber'] = 'House'
            lawmaker_info['party'] = member['party']

    for member in senate_members_data:
        lawmaker_full_name = f'{member["first_name"]} {member["last_name"]}'
        if name in lawmaker_full_name.lower():
            lawmaker_info['name'] = lawmaker_full_name
            lawmaker_info['id'] = member['id']
            lawmaker_info['chamber'] = 'Senate'
            lawmaker_info['party'] = member['party']

    return lawmaker_info

@app.route("/lawmaker-results")
def lawmaker_results():
    lawmaker_query = request.args.get('lawmaker-query')

    lawmaker_info = get_lawmaker_info(lawmaker_query)

    request_URL = f'https://api.propublica.org/congress/v1/members/{lawmaker_info["id"]}/bills/introduced.json'
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(request_URL, headers=headers).json()

    context = {
        'lawmaker_name': lawmaker_info['name'],
        'lawmaker_chamber': lawmaker_info['chamber'],
        'lawmaker_party': lawmaker_info['party']
    }
    return render_template('lawmaker-results.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
