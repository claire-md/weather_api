from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os, requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + API_KEY

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    units = request.form["units"]
    zip = request.form.get("zipcode")
    city = request.form.get("city")

    # Checks if the zipcode entered is 5 digits and is numbers
    if len(zip) == 5 and zip.isdigit():
        complete_url = base_url + "&zip=" + zip + "&units=" + units
        response = requests.get(complete_url)

        res_json = response.json()
        temp = res_json["main"]["temp"]
        description = res_json["weather"][0]["description"]

        return render_template("temperature.html",
                               zipcode=zip,
                               unit=units,
                               temp=temp,
                               description=description)
    elif len(city) > 1 and not city.isdigit():
        complete_url = base_url + "&q=" + city + "&units=" + units
        response = requests.get(complete_url)

        res_json = response.json()
        temp = res_json["main"]["temp"]
        description = res_json["weather"][0]["description"]

        return render_template("temperature.html",
                               city=city,
                               unit=units,
                               temp=temp,
                               description=description)
    else:
        flash("Please enter a valid zipcode", category="error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)