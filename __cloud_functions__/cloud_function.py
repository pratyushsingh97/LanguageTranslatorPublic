import sys
import json
import requests


def main(params):
    utterance = params['data']
    source = params['source']
    target = params['target']
    
    model_id = f"{source}-{target}"
    
    if source != target:
        translated_text = translate(utterance, model_id)
        return {"text": utterance,
                "translated_text": translated_text[0]['translation'], 
                "language": target}
    
    return {"text": utterance,
            "translated_text": utterance, 
            "language": target}

def translate(text, model_id):
    """ Translate the text using the model-id. The model id is {source}-{target}.
    When this function is called in the pre-send hook, the source is user's language and the target is "en".
    When this function is called in the pre-receive hook, the source is "en" and the target is the user's language

    VISIT the IBM cloud documentation on translation: https://cloud.ibm.com/apidocs/language-translator/language-translator#translate

    Args:
        text: the text to be translated.
        model_id: the translation model.
    """
    
    headers = {'Content-Type': 'application/json',}
    params = (('version', '2018-05-01'),)
    url = 'INSTANCE URL'
    api_key = 'API_KEY'

    data = {"text":[text],"model_id": model_id}
    data = json.dumps(data)
    url = url + "/v3/translate" 
    
    response = requests.post(url,
                            headers=headers, 
                            params=params, 
                            data=data, 
                            auth=('apikey', api_key))
    
    if response.status_code == 200:
        try:
            response = json.loads(response.text)
            translations = response['translations']
            
            return translations
            
        except:
            return "Uh Oh! An error has occurred while answering your question. Please try again."
        
    elif response.status_code == 400 or response.status_code == 404:
        return response.text
    
    else:
        return "Uh Oh! An error has occurred while answering your question. Please try again."