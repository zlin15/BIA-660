import os
import json
import requests
import datetime
import time
from flask import Flask, request, Response

application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'zeyang' #e.g. zac_bot
my_slack_username = 'zlin15' #e.g. zac.wentzell
slack_inbound_url = 'https://hooks.slack.com/services/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'

# this handles POST requests sent to your server at SERVERIP:41953/slack
# Send the text content of your enter in Slack to the server using Outgoing Webhook.
@application.route('/slack', methods=['POST'])
def inbound():
    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':taxi:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form
    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message
#The code:
    if username in [my_slack_username, 'zac.wentzell']:

        #============TASK1======================================

        # Your code for the assignment must stay within this if statement
        if text == '&lt;BOTS_RESPOND&gt;':
            response = {
                'username': my_bot_name,
                'icon_emoji': ':pill:',
                'text': 'Hello, my name is zlin_bot. I belong to zlin15. I live at 52.43.135.7.'}

       #=============TASK2 & TASK3===================================================
       # In task3, the question may have to end with '?' and no space between tags.
        #  e.g. <I_NEED_HELP_WITH_CODING>: find duplicates?[python][list]
        if '&lt;I_NEED_HELP_WITH_CODING&gt;:'in text:
            remove_1 = text.replace('][', ';')
            remove_2 = remove_1.replace('[', '')
            remove_3 = remove_2.replace(']', '')
            var1_ori = remove_3.split('?')[0]
            var1 = var1_ori.split(':')[1]
            var2 = remove_3.split('?')[1]         # task3 assign tags to var2 so that they can be inserted to the url
            try:
                get = requests.get('https://api.stackexchange.com/search/advanced', params={'order': 'desc', 'sort': 'relevance', 'q': var1, 'accepted': 'True', 'tagged': var2, 'site': 'stackoverflow', 'run': 'true'})
                ori_api = get.text
                result = json.loads(ori_api)  # result is now a dict
                set=[]
                for i in range(0, 5):
                    title = result['items'][i]['title']
                    link = result['items'][i]['link']
                    answers_count = result['items'][i]['answer_count']
                    u = result['items'][i]['creation_date']
                    creation_time = datetime.datetime.fromtimestamp(u).strftime('%m/%d/%Y')
                    set.append(title + ' ' + link + ' ' + '(' + str(answers_count) + ' Answers' + ')'+', '+creation_time+'new')
                    del_1=str(set).replace("[","")
                    del_2=del_1.replace("]","")
                    del_3 = del_2.replace("u'","")
                    new_line = del_3.replace("new',","\n")
                    response= {
                        'username': my_bot_name,
                        'icon_emoji': ':pill:',
                        'text': new_line.replace("new'", "")}
            except:
                    response={
                        'username': my_bot_name,
                        'icon_emoji': ':pill:',
                        'text': "Didn't find an answer. Please try another question or tag:)"}

        # ===============TASK4===================================
        if "&lt;WHAT'S_THE_WEATHER_LIKE_AT&gt;:" in text:
            var1 = text.split(':')[1]
            get = requests.get(url = 'http://api.openweathermap.org/data/2.5/weather?',params={'q':var1,'appid':'b41bd0a566eba94f06bbf9505f58e24d'})
            ori_api = get.text
            result = json.loads(ori_api)

            #Get api info
            city = result['name']
            country = result['sys']['country']
            weather_descrip = result['weather'][0]['main']
            main_temp= result['main']['temp']
            temp = (main_temp*1.8)-459.69    #  Transform temperature from Kelvin to Fahrenheit
            wind_speed = result['wind']['speed']  # Unit: meter/second
            humidity = result['main']['humidity']  # %
            current_time = int(round(time.time()))
            response={
                "username": my_bot_name,
                "icon_emoji": ":taxi:",
                "attachments": [
                    {
                        "color": "#36a64f",
                        "pretext": "Below is the Weather Forecast for that area:",
                        "title": "Weather Forecast Website Link:",
                        "title_link": 'http://openweathermap.org/api',
                        "text" : 'The area your are looking for is: ' + city +', '+country +'\n'\
                                +"Today's weather :  "  +weather_descrip+'\n'\
                                +'Temperature now: '+str(temp)+' F'+'\n'\
                                +'Wind speed now: ' + str(wind_speed)+' m/s'+'\n'\
                                +'Humidity: '+ str(humidity)+'%',
                        "footer": "Weather API",
                        "footer_icon": 'https://platform.slack-edge.com/img/default_application_icon.png',
                        "ts": current_time
                    }
                ]
           }

 #POST the code OUTPUT from the server to the channel through the incoming webhook.
        if slack_inbound_url and response:
            r = requests.post(slack_inbound_url, json=response)

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
