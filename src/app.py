import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)

config_url = 'https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/resources/data.json'
response = requests.get(config_url)
config = json.loads(response.text)

def check_username(username, platform_config):
    error_type = platform_config.get('errorType', None)
    nsfwtype = platform_config.get('isNSFW', None)
    if error_type == "status_code" and nsfwtype != "true":
        url = platform_config['url'].format(username)

        try:
            res = requests.get(url)
            res.raise_for_status()

            if res.status_code == 200:
                return {"status": "Username Found", "url": url}
        except requests.exceptions.RequestException as e:
            pass

    return {"status": "Skipped", "url": platform_config['url']}
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['user_input']
        response = []
        found_usernames = 0 
        for platform, platform_config in config.items():
            result = check_username(username, platform_config)
            if result["status"] == "Username Found":
                response.append(result)
                found_usernames += 1

            if found_usernames == 30:
                break

        print(response)
        return render_template('index.html', user_input=username, response=response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
