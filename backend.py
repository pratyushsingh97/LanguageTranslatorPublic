""" Written by: Pratyush Singh
This flask function calls out to the translate cloud function, and then passes the response back to the front-end
"""

import requests
import json
import pickle
from pprint import pprint
from collections import defaultdict

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# translate = None

@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
	return render_template('homepage.html')


@app.route('/translate', methods=['POST'])
@cross_origin()
def translate():
	""" Calls out to the translate cloud function.
	The translate route takes to query parameters: 'source' and 'target'
	The 'source' parameter is the language code for the utterance language, 
	and the 'target' parameter is the language code for the language the utterances needs
	to be translated into. It returns the response from the cloud function.
	Args: None 
	Returns:
	- translation_results: a dictionary containing the translation from the cloud function
	"""

	source = request.args.get('source')
	target = request.args.get('target')

	utterances = json.loads(request.args.get('utterances'))
	utterances = utterances['translation']
	translation_results = []
	
	header = {'Accept': 'application/json', 
			  'Content-type': 'application/json'
			}

	for utterance in utterances:
		body = {
		"source": source,
		"target": target,
		"data": utterance
	}

		body = json.dumps(body)
		response = requests.post(url="CF_URL" # CF URL API
								data=body,
								headers=header)

		response = defaultdict(dict, json.loads(response.text))
		translation_results.append(response['translated_text'])

	return {"results": translation_results}

		

if __name__ == '__main__':
		app.run(port=4000, debug=True)