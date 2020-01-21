import requests
import argparse

parser = argparse.ArgumentParser(description='Specify the query parameters.')
parser.add_argument('-lang', '--language', help='The language to be queried.')
parser.add_argument('-min_stars', '--min_stars', help='The minimal number of starts to be queried.')
parser.add_argument('-user', '--username', help='The username from Github API.')
parser.add_argument('-token', '--auth_token', help='The authorization token from Github API.')
args = parser.parse_args()

api_url =  'https://api.github.com/search/repositories'
page = 1

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

f = open('java_repositories.txt', 'w')

repos = []

while True:
    request_url = api_url + str(page)
    print(request_url)
    request = requests.get(request_url, params=[], auth=(args.username, args.auth_token))
    if request.status_code == 200:
        repositories = request.json()
        if repositories:
            for item in repositories['items']:
                if item['description'] != None:
                    repos.append([item['stargazers_count'], item['full_name'] + ' | ' + item['description']])  
                else:
                    repos.append([item['stargazers_count'], item['full_name'] + ' | No description available'])  
            page += 1
        else:
            print('Empty JSON')
            break
    else:
        print('Status code = ' + str(request.status_code))
        break

sorted_repos = sorted(repos, reverse=True)
print(sorted(repos, reverse=True))
for item in sorted_repos:
    f.write(item[1] + '\n')
    