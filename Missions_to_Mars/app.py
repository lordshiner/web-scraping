from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.NEWS

@app.route("/")
def index():
    
    listings = db.NEWS.find_one()
    return render_template("index.html" , listings = listings)

@app.route("/scrape")
def scraper():
    listing_data = scrape_mars.scrape()
    collection = db.NEWS
    collection.update_one({"Ltitle":listing_data["Ltitle"]},{'$set':listing_data}, upsert = True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    