import requests
import json
import time
import pandas as pd
import sqlalchemy

#TODO: Update token_file path (should be in JSON format)
token_file = r'C:\Users\vamsh\Desktop\temp\tokens.txt'

tokens = {}

with open(token_file) as f:
    tokens = json.loads(f.read())

BEARER_TOKEN = tokens['Bearer Token']

TARGET_TABLE = 'tweets'
TARGET_SCHEMA = 'dbo' # Using default dbo for simplicity.

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def define_sql_engine(sql_server_name, target_db_name):

    # Setup the connection Engine
    engine = sqlalchemy.create_engine(f'mssql+pyodbc://{sql_server_name}/{target_db_name}?driver=SQL+Server')

    return engine

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )

    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )

    print(json.dumps(response.json()))


def set_rules():
    '''
        Sets the Justin Bieber rule and returns True if the rule was applied properly, and False if not.
        Filtering out Music related tweets using Twitters Context Annotation -
            54: Musician, 84: Book Music Genre, 89: Music Album
        Only excluding 89.* because volume of tweets is very limited when Musician, and/or Book Music Genre
        are also excluded.
    '''
    rules = [
        {"value": "-context:89.* -is:retweet (\"Justin Bieber\") lang:en"}
    ]
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )

    resp_json = response.json()

    # The response should have a 'data' key
    if 'data' in resp_json:
        print(json.dumps(resp_json))
        return True

    return False


def get_stream(sql_engine):
    tweet_fields = 'id,text,author_id,conversation_id,created_at'
    response = requests.get(
        f"https://api.twitter.com/2/tweets/search/stream?tweet.fields={tweet_fields}"
        , auth=bearer_oauth, stream=True,
    )
    print(response.status_code)

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            load_tweet(json_response, sql_engine)


def load_tweet(tweet_json, sql_engine):
    tweet_dict = tweet_json['data']
    data ={
        'author_id' : [tweet_dict['author_id']],
        'conversation_id' : [tweet_dict['conversation_id']],
        'id' : [tweet_dict['id']],
        'text' : [tweet_dict['text']],
        'created_at' : [tweet_dict['created_at']]
    }
    df = pd.DataFrame(data)
    print(df.columns)
    df.to_sql(TARGET_TABLE, sql_engine, if_exists='append', schema=TARGET_SCHEMA, index=False,
              chunksize=25, method='multi')



def main():
    '''
        This script is safe to rerun without any prior cleanup.
        All rules will be deleted first, and then regenerated at run time.
    '''
    sql_engine = define_sql_engine(sql_server_name='DESKTOP-QB0RL6F\SQLEXPRESS',
                                   target_db_name='WalmartAssessment')
    rules = get_rules()
    delete_all_rules(rules)
    # If the rule is not properly applied, exit out of script
    if not bool(set_rules()):
        quit()
    time.sleep(3) # Giving Twitter a few seconds to register and spin up the rule
    get_stream(sql_engine)


if __name__ == "__main__":
    main()