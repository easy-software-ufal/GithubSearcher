import requests
import argparse
import json

parser = argparse.ArgumentParser(description='Specify the query parameters.')
parser.add_argument('-lang', '--language', help='The language to be queried.')
parser.add_argument('-min_stars', '--min_stars', help='The minimal number of starts to be queried.')
parser.add_argument('-user', '--username', help='The username from Github API.')
parser.add_argument('-token', '--auth_token', help='The authorization token from Github API.')
args = parser.parse_args()

api_url =  'https://api.github.com/search/repositories'
page = 1
data = {}

if (args.language != None) and (args.min_stars != None):
    api_url += '?q=language:' + str(args.language) + '+stars:>=' + str(args.min_stars)
elif (args.min_stars != None) and (args.language == None):
    api_url += '?q=stars:>=' + str(args.min_stars)
elif (args.language != None) and (args.min_stars == None):
    api_url += '?q=language:' + str(args.language)    

if args.language or args.min_stars:
    api_url += '+sort:true&page='
else:
    api_url += '?q=sort:true&page='

repos = []

while True:
    request_url = api_url + str(page)
    print('Searching for ' + request_url)
    request = requests.get(request_url, params=[], auth=(args.username, args.auth_token))
    if request.status_code == 200:
        repositories = request.json()
        if repositories:
            for item in repositories['items']:
                if item['description'] != None:
                    repos.append([item['stargazers_count'], item['full_name'], item['description'], item['html_url']])  
                else:
                    repos.append([item['stargazers_count'], item['full_name'], 'No description available', item['html_url']])
            page += 1
            print('Done in the page ' + str(page))
        else:
            print('Empty JSON')
            break
    else:
        print('Status code = ' + str(request.status_code))
        break

print('Sorting results...')

sorted_repos = sorted(repos, reverse=True)

for item in sorted_repos:
    data[item[1]] = []
    data[item[1]].append({
        'stars': item[0],
        'description': item[2],
        'link': item[3]
    })

print('Printing JSON file...')

with open('outfile.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)

print('Done!')