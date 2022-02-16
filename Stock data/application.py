from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for,Response
from flask_session import Session
from bs4 import BeautifulSoup
import requests



# this is created by Sushanta Neupane

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def home():
    return redirect("/data")



@app.route("/data", methods=["GET", "POST"])
def data():
    # Site URL
    url="https://merolagani.com/LatestMarket.aspx"
    
    # make a Get request to fentch the raw HTML data
    con = requests.get(url)
    soup = BeautifulSoup(con.text,'lxml') #code of the page
    table = soup.find('table', class_="table table-hover live-trading sortable") #table of data
    headers = [i.text for i in table.find_all ('th')] #data of the th tag
    # print(headers)
    data = [j for j in table.find_all('tr', {"class" : ["decrease-row","increase-row","nochange-row"]})] #data inside the tr tag
    
    # making in the formate of list like [{'name':'ADCL', 'LTP':'123'}]
    
    result = [{headers[index]:cell.text for index,cell in enumerate(row.find_all ("td"))} for row in data]

    # this is the result
    result = [{headers[index]:cell.text for index,cell in enumerate(row.find_all("td"))} for row in data ]
    fullname = [j.get('title') for j in table.find_all('a', {"target":["_blank"]})]
    new =[{'Name':fullname[kk],'Symbol': result[kk]['Symbol'], 'LTP': result[kk]['LTP'], 'LTV': result[kk]['LTV'], 'Change': result[kk]['% Change'], 'High': result[kk]['High'], 'Low': result[kk]['Low'], 'Open': result[kk]['Open'], 'Qty.': result[kk]['Qty.']} for kk in range(len(fullname))]

    

    return render_template("stock.html",new=new)

if __name__ == '__main__':
      app.run()
