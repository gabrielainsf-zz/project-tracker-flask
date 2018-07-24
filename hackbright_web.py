"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect

import hackbright

app = Flask(__name__)

# add secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


#### Searching and seeing student into
@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    return render_template("student_info.html", first=first, last=last, github=github)


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


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
