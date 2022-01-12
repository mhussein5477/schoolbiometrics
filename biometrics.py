import json
import requests


url="https://portal.zettatel.com/SMSApi/send"
headers={'Content-type':'application/json','Accept':'application/json'}
data={
	"userid": "adamrashid",
	"password" : "bJmVYrVY",
	"senderid": "Notify_MSG",
	"msgType": "text",
	"duplicatecheck": "true",
	"sms": [
			{
      		"mobile": ["+254748370216"],
      		"msg": "Rorooooo, inkubali, Alhamdulillah"
    		}
  	]
}
r=requests.post(url,data=json.dumps(data),headers=headers)
response = json.loads(r.content)
print(response)