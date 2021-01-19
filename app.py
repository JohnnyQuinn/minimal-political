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
        'full_congress_list': full_congress_list    ,                   
    }

    return render_template('home.html', **context)

def create_members_list(member_data1, member_data2):
    """creates list of members from both senate and house along with their ids"""
    member_list = []
    for member in member_data1:
        fullname = {
            "first_name": member['first_name'],
            "last_name": member['last_name'],
            "id": member['id']
        }
        member_list.append(fullname)
    for member in member_data2:
        fullname = {
            "first_name": member['first_name'],
            "last_name": member['last_name'],
            "id": member['id']
        }
        member_list.append(fullname)
    
    JSON_member_list = {
        "full_congress_list": member_list
    }

    return JSON_member_list

def get_lawmaker_info(lawmaker_query, senate_members_data, house_members_data):
    """ takes in user inputted name of a lawmaker and returns the lawmaker's info (full name, chamber, id, party)"""

    lawmaker_info = {
        'name': '',
        'id': '',
        'chamber': '',
        'party': ''
    }
    lawmaker_query = lawmaker_query.lower()
    """
    # TODO: update the condition to match the name search so that;
        - it doesn't think its MacHenry when the query was henry 
    """
    # matches query based on name in the senate 
    for member in senate_members_data:
        lawmaker_full_name = f'{member["first_name"]} {member["last_name"]}'
        if lawmaker_query in lawmaker_full_name.lower():
            lawmaker_info['name'] = lawmaker_full_name
            lawmaker_info['id'] = member['id']
            lawmaker_info['chamber'] = 'Senate'
            lawmaker_info['party'] = member['party']
            break 
    # if not in the senate then check the house
        else: 
            for member in house_members_data:
                lawmaker_full_name = f'{member["first_name"]} {member["last_name"]}'
                if lawmaker_query in lawmaker_full_name.lower():
                    lawmaker_info['name'] = lawmaker_full_name
                    lawmaker_info['id'] = member['id']
                    lawmaker_info['chamber'] = 'House'
                    lawmaker_info['party'] = member['party']
                    break

    # corrects lawmaker's party 
    if lawmaker_info['party'] == 'R':
        lawmaker_info['party'] = 'Republican'
    elif lawmaker_info['party'] == 'D':
        lawmaker_info['party'] = 'Democrat'
    else:
        lawmaker_info['party'] = 'Independent'

    return lawmaker_info

@app.route("/lawmaker-results")
def lawmaker_results():
    # [ProPublica] GET list of members in senate and house 
    # TODO: put API-key in .env and .gitignore
    senate_members_url = "https://api.propublica.org/congress/v1/116/senate/members.json"
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(senate_members_url, headers=headers).json()

    senate_members_data = r["results"][0]["members"]

    house_members_url = "https://api.propublica.org/congress/v1/116/house/members.json"

    r = requests.get(house_members_url, headers=headers).json()

    house_members_data = r["results"][0]["members"]

    # get user inputted query from searchbar
    lawmaker_query = request.args.get('lawmaker-query')

    # get their info (id, name, chamber, party)
    lawmaker_info = get_lawmaker_info(lawmaker_query, senate_members_data, house_members_data)

    print(f'- {lawmaker_info["name"]}\n- {lawmaker_info["id"]}')

    # [ProPublica] GET dictionary of the last 20 most recent bills voted on based on lawmakers's id 
    # TODO: put API-key in .env and .gitignore
    request_URL = f'https://api.propublica.org/congress/v1/members/{lawmaker_info["id"]}/votes.json'
    headers = {'x-api-key': "Hk6QVaUEQ453sdhadQMafiX9Ya5hblL7uwqVPEFw"}

    r = requests.get(request_URL, headers=headers).json()

    recent_votes = r['results'][0]['votes']

    recent_votes = filter_votes(recent_votes)

    context = {
        'lawmaker_name': lawmaker_info['name'],
        'lawmaker_chamber': lawmaker_info['chamber'],
        'lawmaker_party': lawmaker_info['party'],
        'lawmaker_id': lawmaker_info['id'],
        'recent_votes': recent_votes
    }
    return render_template('lawmaker-results.html', **context)

def filter_votes(recent_votes):
    """filter through api response for votes and get votes only on bills (and not other stuff) """
    recent_votes_final = []

    for vote in recent_votes:
        if bool(vote['bill']) is not False: #if this dictionary is not empty
            if vote['bill']['title'] is not None: #if the bill title isnt null
                vote_info = {
                    'title': vote['bill']['title'],
                    'date': vote['date'],
                    'position': vote['position']
                }
                recent_votes_final.append(vote_info)
            elif 'nomination' in vote.keys(): #if the bill title is null and there is a nomination dictionary
                if vote['question'] == "On the Nomination": #if the vote is for the nomination
                    vote_info = {
                        'title': f'{vote["question"]} of {vote["description"]}',
                        'date': vote['date'],
                        'position': vote['position']
                    }
                    recent_votes_final.append(vote_info)
    
    return recent_votes_final

if __name__ == '__main__':
    app.run(debug=True)
