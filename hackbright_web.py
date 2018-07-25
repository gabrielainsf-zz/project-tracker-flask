"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect

import hackbright

app = Flask(__name__)

# add secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/")
def show_homepage():
    """Display homepage."""
    # get all students from db (list of tuples with first name, last name)
    students = hackbright.get_students()

    # get all projects from db
    projects = hackbright.get_projects()

    return render_template("index.html", all_students=students, all_projects=projects)




#### Searching and seeing student into
@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", first=first, last=last, 
    						github=github, projects=projects)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


#### Adding new student(s)
@app.route("/student-form")
def student_form():
	"""Collect info for new student."""
	# render a template with an HTML form
	return render_template("student_form.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    
    # collect form info
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    # use form into to call make_new_student
    hackbright.make_new_student(first_name, last_name, github)

    # flash message and redirect to /student-form route
    flash("Successfully added {} {}".format(first_name, last_name))
    return redirect("/student-form")


@app.route("/project")
def show_project_info():
	""" Displays project information."""

    # get project title from GET request
	project_title = request.args.get('title')

    # get information about project from db
	project_info = hackbright.get_project_by_title(project_title)

    # get student project grades from db
	student_projects = hackbright.get_grades_by_title(project_title)

    # pass this information to the template (for displaying project info)
	return render_template("project_info.html", project_info=project_info,
							students=student_projects)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
