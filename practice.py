import requests
import json

session = requests.Session()

r = session.post("https://staging.transitexec.com/Account/LogOn", 
	data={"UserName":"ito-bjfyan",
	"Password":"ayylmao",
	"RememberMe":"false"})

cookie = {"transitconnectgroupMaxQuantityQueryResults":"100","tenantname":"Little Brothers Upper Michigan Chapter",
"tenantid":"249","multitenant":"0","database":"TransitMain"}
cookie.update(session.cookies.get_dict())


g = requests.get("https://staging.transitexec.com/ride/API_RidesByDate/?_dc=1573922316819&date=11%2F1%2F2019&driverid=0&start=0&limit=15&readingID=0.23303928229798543", cookies=cookie)
data = json.loads(g.text)

htmlPage = open("lbfe-demo.html", "w")
htmlPage.write("<html>\n")
htmlPage.write("<head>\n")
htmlPage.write("""<link rel="stylesheet" href="style.css">\n""")
htmlPage.write("</head>")
htmlPage.write("<body>")
htmlPage.write("<table>")
# Write table headers
htmlPage.write("<tr>\n")
htmlPage.write("<th>Name</th>\n")
htmlPage.write("<th>Departing Location</th>\n")
htmlPage.write("<th>Destination</th>\n")
htmlPage.write("<th>Driver</th>\n")
htmlPage.write("</tr>\n")



dataLen = 3
if len(data.get("data")) < 3:
	dataLen = len(data.get("data"))

for i in range(0,dataLen):
	row = data.get("data")[i]
	htmlPage.write("<tr>\n")
	htmlPage.write("<td>" + row.get("customerfullname") + "</td>\n")
	htmlPage.write("<td>" + row.get("legs")[0].get("fromaddr").get("address1") + ", " + row.get("legs")[0].get("fromaddr").get("city") + "</td>\n")
	htmlPage.write("<td>" + row.get("legs")[0].get("toaddr").get("address1") + ", " + row.get("legs")[0].get("toaddr").get("city") + "</td>\n")
	htmlPage.write("<td>" + row.get("legs")[0].get("driver") + "</td>\n")
	htmlPage.write("</tr>\n")
htmlPage.write("</table>\n")

weatherFile = open("weatherwidget.txt", "r")
htmlPage.write(weatherFile.read())

htmlPage.write("</body>")
htmlPage.write("</html>")