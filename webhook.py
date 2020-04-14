import json #to convert list and dictionary to json
import os
import requests
from flask import Flask #it is microframework to develop a web app
from flask import request
from flask import make_response
#Falsk app for our web app
app=Flask(__name__)
# app route decorator. when webhook is called, the decorator would call the functions which are e defined
@app.route('/webhook', methods=['POST'])
def webhook():
    #convert the data from json.
    req=request.get_json(silent=True, force=True)
    print(json.dumps(req,indent=4))
    # extract the relevant information and use api and get the response and send it dialogflow.
    # #helper function
    res=make_response(req)
    res=json.dumps(res, indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r
# extract parameter values, query weahter api, construct the resposne
def makeResponse(req):
    result=req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q=hyderabad,in&appid=db91df44baf43361cbf73026ce5156cb')
    json_object=r.json()
    weather=json_object['list']
#for i in range(0,40): # if date in weather[i]['dt_txt']:
    #condition=weather[i]['weather'][0]['description']
    condition=weather[0]['weather'][0]['description']
    speech="The forecast for "+city+ " for "+date+" is "+ condition
    return{
        "fulfillmentMessages":[
            { "text":
                  { "text": speech } }]}
    #return { # "speech": speech, # "displayText":speech, # "source":"apiai-weather-webhook"}
if __name__=='__main__':
    port=int(os.getenv('PORT',5000))
    print("starting on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

