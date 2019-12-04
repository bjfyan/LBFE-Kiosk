import requests
import json

session = requests.Session()

r = session.post("https://staging.transitexec.com/Account/LogOn", 
	data={"UserName":"lewiszac",
	"Password":"nemt123",
	"RememberMe":"false"})

cookie = {"transitconnectgroupMaxQuantityQueryResults":"100","tenantname":"FDS Enterprises",
"tenantid":"300","multitenant":"0","database":"TransitMain"}
cookie.update(session.cookies.get_dict())


g = requests.get("https://staging.transitexec.com/ride/API_RidesByDate/?_dc=1573922316819&date=12%2F1%2F2019&driverid=0&start=0&limit=15&readingID=0.23303928229798543", cookies=cookie)
data = json.loads(g.text)

htmlPage = open("lbfe-demo.html", "w")
htmlPage.write("<html>\n")
htmlPage.write("<head>\n")
htmlPage.write("""<link rel="stylesheet" href="style.css">\n""")
htmlPage.write("</head>")
htmlPage.write("<body>")
htmlPage.write("<table>")
# Write table headers
headerList = {"Time", "Name", "Departing Location", "Destination", "Driver"}
htmlPage.write("<tr>\n")
for item in headerList:
	htmlPage.write("<th>" + item + "</th>\n")
htmlPage.write("</tr>\n")


# Get only first five for testing purposes
dataLen = 10
if len(data.get("data")) < dataLen:
	dataLen = len(data.get("data"))

rideData = []
for i in range(0, dataLen):
	row = data.get("data")[i]
	if row.get("legs")[0].get("cancelstatus") == True:
		continue
	rideData.append({"Time":row.get("legs")[0].get("appointmenttime"),
					 "Name":row.get("customerfullname"), 
	                 "Departing Location":row.get("legs")[0].get("fromaddr").get("address1") + ", " + row.get("legs")[0].get("fromaddr").get("city"),
	                 "Destination":row.get("legs")[0].get("toaddr").get("address1") + ", " + row.get("legs")[0].get("toaddr").get("city"),
	                 "Driver":row.get("legs")[0].get("driver")})


for i in range(0,len(rideData)):
	row = rideData[i]
	htmlPage.write("<tr>\n")
	for item in headerList:
		htmlPage.write("<td>" + row.get(item) + "</td>\n")
	htmlPage.write("</tr>\n")
htmlPage.write("</table>\n")

weatherFile = open("weatherwidget.txt", "r")
htmlPage.write(weatherFile.read())

htmlPage.write("</body>")
htmlPage.write("</html>")