#Imports
from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os

#Setup variables
app = Flask(__name__)
title = "To Do List"
heading = "To Do List"

#host Uniform Resource Identifier
client = MongoClient("mongodb://localhost:27017") #for the default local host on your machine, if hosted elsewhere, update appropriately.
#Select database
db = client.testdb
#Select collection name
todos = db.todo

#Note that if the database and collection aren't yet created, they will be automatically by these delcarations

def redirect_url():
	#redirects to the index page
	return request.args.get('next') or \
	request.referrer or \
	url_for(index)

@app.route("/list")
def lists ():
	#display all todos
	todos_1 = todos.find() #find all todos in the collection
	a1 = "active" #set the selection to active, this indicates which section of the list the user is on
	return render_template('index.html',a1=a1,todos=todos_1,t=title,h=heading)
		
@app.route("/")
@app.route("/incomplete")
def tasks ():
	#Display uncompleted todos
	todos_1 = todos.find({"done":"no"}) #find all todos where the done field shows "no"
	a2 = "active" #set the selection to active, this indicates which section of the list the user is on
	return render_template('index.html', a2=a2, todos=todos_1,t=title,h=heading)
	
@app.route("/completed")  
def completed ():  
    #Display the Completed Tasks  
    todos_l = todos.find({"done":"yes"}) #find all todos where the done field shows "yes" 
    a3="active"  #set the selection to active, this indicates which section of the list the user is on
    return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)  
 
@app.route("/done")  
def done ():  
    #Done-or-not ICON
    #When you click on the icon, changes the status of the item by updating the database
    id=request.values.get("_id")  
    task=todos.find({"_id":ObjectId(id)})  
    if(task[0]["done"]=="yes"):  
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})  
    else:  
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})  
    redir=redirect_url()      
  
    return redirect(redir)  
 
@app.route("/action", methods=['POST'])  
def action ():  
    #Adding a Task  
    name=request.values.get("name")  
    desc=request.values.get("desc")  
    date=request.values.get("date")  
    pr=request.values.get("pr")  
    todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})  
    return redirect("/list")  
 
@app.route("/remove")  
def remove ():  
    #Deleting a Task with various references  
    key=request.values.get("_id")  
    todos.remove({"_id":ObjectId(key)})  
    return redirect("/")  
 
@app.route("/update")  
def update ():  
    id=request.values.get("_id")  
    task=todos.find({"_id":ObjectId(id)})  
    return render_template('update.html',tasks=task,h=heading,t=title)  
 
@app.route("/action3", methods=['POST'])  
def action3 ():  
    #Updating a Task with various references  
    name=request.values.get("name")  
    desc=request.values.get("desc")  
    date=request.values.get("date")  
    pr=request.values.get("pr")  
    id=request.values.get("_id")  
    todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})  
    return redirect("/")  
 
@app.route("/search", methods=['GET'])  
def search():  
    #Searching a Task with various references  
  
    key=request.values.get("key")  
    refer=request.values.get("refer")  
    if(key=="_id"):  
        todos_l = todos.find({refer:ObjectId(key)})  
    else:  
        todos_l = todos.find({refer:key})  
    return render_template('searchlist.html',todos=todos_l,t=title,h=heading)
	
if __name__ == "__main__":  
	app.run()