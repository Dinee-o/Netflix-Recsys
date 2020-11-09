import numpy as np
from flask import Flask, request, make_response
import json
import pickle
from flask_cors import cross_origin
import pandas as pd


app = Flask(__name__)
model = pickle.load(open('RecSys.pkl', 'rb'))

@app.route('/')
def hello():
    return 'Hello World'

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()


def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):

    #sessionID=req.get('responseId')
    result = req.get("queryResult")
     #user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    title1 = parameters.get("title1")
    rating1 = parameters.get("rating1")
    title2 = parameters.get("title2")
    rating2 = parameters.get("rating2")
    title3 = parameters.get("title3")
    rating3 = parameters.get("rating3")

    features =  [
            {'title':title1, 'rating':rating1},
            {'title':title2, 'rating':rating2},
            {'title':title3, 'rating':rating3},
         ] 
    final_features = pd.DataFrame(features)
    intent = result.get("intent").get("displayName")


    if(intent == 'moviesAndRatings'):
        output = movies.loc[movies['movieId'].isin(recommendationTable_df.head(5).keys())]
        fulfillmentText = "Check out these movies, you'll like them.......\n{}".format(output)

    
if __name__=='__main__':
    app.run()