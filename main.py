from flask import Flask, render_template, request, redirect, url_for,make_response
import csv, io

app = Flask(__name__)

# In-memory storage for the submitted data
user_data = []

@app.route("/", methods=["GET", "POST"])
def details_form():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        location = request.form["location"]
        
        # Store the data in the list
        user_data.append({"username": username, "name": name, "location": location})
        
        # Redirect to thank you page or some confirmation
        return redirect(url_for('thank_you'))
    
    return render_template("details.html")

@app.route("/thankyou")
def thank_you():
    return "<h2>Thank you for submitting your details!</h2>"

@app.route("/admin")
def admin():
    return render_template("admin.html", user_data=user_data)

@app.route("/download")
def download_csv():
    # Create a CSV in-memory string
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Username", "Name", "Location"])
    
    # Write all user data to the CSV
    for user in user_data:
        writer.writerow([user["username"], user["name"], user["location"]])
    
    # Prepare the response as a CSV file
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=user_data.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

if __name__ == "__main__":
    app.run(debug=True)
