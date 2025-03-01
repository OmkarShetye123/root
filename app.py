from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Reports(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(50))
    desc = db.Column("description", db.String())
    link = db.Column("link", db.String())

    def __repr__(self):
        return f'<Report {self.title}>'

class Projects(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(50))  # Fixed column name
    desc = db.Column("description", db.String())
    link = db.Column("link", db.String())

    def __repr__(self):
        return f'<Project {self.title}>'

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/insight")
def insight():
    all_reports = Reports.query.all() 
    return render_template('insight.html',reports=all_reports)


@app.route("/add-report", methods=["GET", "POST"])
def add_report():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        link = request.form["link"]

        new_report = Reports(title=title, desc=desc, link=link)
        db.session.add(new_report)
        db.session.commit()

        return redirect("/")  # Redirect to home after adding

    return render_template("add_report.html")

@app.route("/archive")
def archive():
    all_archives = Projects.query.all() 
    return render_template('archive.html', archives=all_archives)

@app.route("/add-archive", methods=["GET", "POST"])
def add_archive():
    if request.method == "POST":
        name = request.form["title"]
        desc = request.form["desc"]
        link = request.form["link"]

        new_archive = Projects(title=name, desc=desc, link=link)
        db.session.add(new_archive)
        db.session.commit()

        return redirect("/")  # Redirect to home after adding

    return render_template("add_Archive.html")

@app.route("/search", methods=["GET"])
def search():
    search_query = request.args.get("search", "")

    reports = Reports.query.filter(Reports.title.contains(search_query)).all()
    projects = Projects.query.filter(Projects.title.contains(search_query)).all()

    return render_template('search.html', reports=reports, projects=projects, search_query=search_query)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensures tables are created before running
    app.run(debug=True)
