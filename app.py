# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    Mars_Data_From_MongoDB = mongo.db.collection.find()

    # Return template and data
    return render_template("index.html", NASA_Mars_Data=Mars_Data_From_MongoDB)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    Mars_Data=scrape_mars.scrape()
    print(Mars_Data)
    print(Mars_Data['News_Title'])
    print(Mars_Data['News_Para'])

    Mars_Dict ={
        'News_Title' : Mars_Data['News_Title'] ,
        'News_Para' : Mars_Data['News_Para']    
    }
    
    mongo.db.collection.drop()
    mongo.db.collection.insert_one(Mars_Dict)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


