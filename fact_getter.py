import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from starlette.responses import UJSONResponse
from starlette.status import HTTP_200_OK
from ujson import loads

app = FastAPI(title='Fact Getter',
              description='This is a meta API that aggregates various API\'s '
                          'into a single unified interface.')


@app.get("/cat", content_type=UJSONResponse)
def cat_fact():
    r = requests.get(url='https://catfact.ninja/fact')
    return {'fact': loads(r.content)['fact']}


@app.get("/kanye", content_type=UJSONResponse)
def kanye_fact():
    r = requests.get(url='https://api.kanye.rest')
    return {'fact': loads(r.content)['quote']}


@app.get("/inspirational", content_type=UJSONResponse)
def inspirational_quote():
    r = requests.get(url='https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    return {'fact': loads(r.content)['quoteText']}


@app.get("/design", content_type=UJSONResponse)
def design_quote():
    r = requests.get(url='http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1')
    soup = BeautifulSoup(loads(r.content)[0]['content'], 'lxml')
    return {'fact': soup.get_text(strip=True)}


@app.get("/simpsons", content_type=UJSONResponse)
def simpsons_quote():
    r = requests.get(url='https://thesimpsonsquoteapi.glitch.me/quotes')
    return {'fact': loads(r.content)[0]['quote']}


@app.get("/_ah/warmup", status_code=HTTP_200_OK, include_in_schema=False)
def warmup():
    return {'Response Code': '418'}
