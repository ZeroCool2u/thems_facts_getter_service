import logging
import os

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from google.cloud import firestore
from google.cloud.exceptions import NotFound
from orjson import loads
from starlette.status import HTTP_200_OK

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d-%Y %I:%M:%S %p', level=logging.WARNING)

if not os.getenv('GAE_ENV', '').startswith('standard') and os.getenv('GITHUB_WORKFLOW') is None:
    os.environ[
        'GOOGLE_APPLICATION_CREDENTIALS'] = r'/home/theo/PycharmProjects/thems_facts/getter_service/facts-sender-owner.json'

elif os.getenv('GITHUB_WORKFLOW') is not None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.getenv('HOME'), 'facts-sender-owner.json')


def gcp_support() -> dict:

    try:
        db = firestore.Client()
        api_keys_ref = db.collection(u'api_keys').document(u'gvRhG4XnOHccmty4UoBU')
        doc = api_keys_ref.get()
        api_keys = doc.to_dict()
        logging.info('API Keys successfully retrieved.')
        return api_keys
    except NotFound as e:
        api_keys = {'twilio_sid': 'TWILIO_SID_NOT_FOUND'}
        logging.error(f'The API keys could not be retrieved from Firestore: {str(e)}')
        return api_keys
    except Exception as e:
        api_keys = {'twilio_sid': 'TWILIO_SID_NOT_FOUND'}
        logging.error(f'Firestore client failed to init. The fact getter service will run in local only mode: {str(e)}')
        return api_keys


API_KEYS = gcp_support()

app = FastAPI(title='Fact Getter',
              description='This is a meta API that aggregates various API\'s '
                          'into a single unified interface.')


@app.get("/cat", response_class=ORJSONResponse)
async def cat_fact():
    r = requests.get(url='https://catfact.ninja/fact')
    return {'fact': loads(r.content)['fact']}


@app.get("/kanye", response_class=ORJSONResponse)
async def kanye_fact():
    r = requests.get(url='https://api.kanye.rest')
    return {'fact': loads(r.content)['quote']}


@app.get("/inspirational", response_class=ORJSONResponse)
async def inspirational_quote():
    r = requests.get(url='https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    return {'fact': loads(r.content)['quoteText']}


@app.get("/design", response_class=ORJSONResponse)
async def design_quote():
    r = requests.get(url='https://quotesondesign.com/wp-json/wp/v2/posts/?orderby=rand')
    soup = BeautifulSoup(loads(r.content)[0]['content']['rendered'], 'lxml')
    return {'fact': soup.get_text(strip=True)}


@app.get("/simpsons", response_class=ORJSONResponse)
async def simpsons_quote():
    r = requests.get(url='https://thesimpsonsquoteapi.glitch.me/quotes')
    return {'fact': loads(r.content)[0]['quote']}


@app.get("/swanson", response_class=ORJSONResponse)
async def swanson_quote():
    r = requests.get(url='http://ron-swanson-quotes.herokuapp.com/v2/quotes')
    return {'fact': loads(r.content)[0]}


@app.get("/norris", response_class=ORJSONResponse)
async def chuck_norris_fact():
    r = requests.get(url='https://api.chucknorris.io/jokes/random')
    return {'fact': loads(r.content)['value']}


@app.get("/shitty-trump", response_class=ORJSONResponse)
async def trump_quote():
    r = requests.get(url='https://api.tronalddump.io/random/quote')
    return {'fact': loads(r.content)['value']}


@app.get("/random_gif", response_class=ORJSONResponse)
async def rand_gif():
    giphy_api_key: str = API_KEYS['giphy_api_key']
    r = requests.get(url=f"http://api.giphy.com/v1/gifs/trending?api_key={giphy_api_key}&limit=1")
    return {'fact': loads(r.content)['data'][0]['images']['looping']['mp4']}


@app.get("/dad_joke", response_class=ORJSONResponse)
async def rand_dad():
    r = requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
    return {'fact': loads(r.content)['joke']}


@app.get("/_ah/warmup", status_code=HTTP_200_OK, include_in_schema=False)
async def warmup():
    return {'Response Code': '418'}
