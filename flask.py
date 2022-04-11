from flask import Flask, render_template
import requests, json

app = Flask(__name__)
resp=requests.get("https://api.thingspeak.com/channels/1275133/feeds.json?results=10")

print(resp.text)
results=json.loads(resp.text)
for temp in results['feeds']:
    temperature = temp['field1']
    print("Temperature:", temperature)

for i in range(10):
    print("downloaded data",i,"temperature =",results["feeds"][i]["field1"])

@app.route("/update/data=<data>", methods=['GET'])
def update(data):
    return render_template("test.html", data = temperature)

if __name__=="__main__":
    app.run(debug=True)