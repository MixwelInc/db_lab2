from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "MongoDB Application"
heading = "Lab 2 Savchenko"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.lab2   #Select the database
series = db.series  #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')
		   
@app.route("/")
@app.route("/list")
def lists ():
	#Display the all Tasks
	series_l = series.find()
	a1="active"
	return render_template('index.html',a1=a1,series=series_l,t=title,h=heading)


@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	title=request.values.get("title")
	premiere=request.values.get("premiere")
	rating=request.values.get("rating")
	series.insert_one({ "title":title, "premiere":premiere, "rating":rating})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	series.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	title=request.values.get("title")
	premiere=request.values.get("premiere")
	rating=request.values.get("date")
	id=request.values.get("_id")
	series.update({"_id":ObjectId(id)}, {'$set':{ "title":title, "premiere":premiere, "rating":rating}})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		series_l = series.find({refer:ObjectId(key)})
	else:
		series_l = series.find({refer:key})
	return render_template('searchlist.html',series=series_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
