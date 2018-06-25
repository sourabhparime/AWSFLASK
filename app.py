import db_helper
from analysis import magic as m
from schema import *
from __init__ import *
import csv, json

file_headers = {}

# Frontend
app.url_map.add(Rule('/', endpoint='register'))
app.url_map.add(Rule('/auth/register', endpoint='register', methods=['POST', 'GET']))
app.url_map.add(Rule('/auth/appstack', endpoint='appstack', methods=['POST', 'GET']))
app.url_map.add(Rule('/thankyou', endpoint='thankyou', methods=['POST', 'GET']))
app.url_map.add(Rule('/salary', endpoint='salary', methods=['POST', 'GET']))


@app.endpoint('register')
def register():
    if request.method == 'POST':
        try:
            db_helper.clear_all_tables()
            # clear the previous session
            session.clear()
            # printing out the request parameters
            print(request.form)
            # converting immutable dict to normal dict
            form_dict = request.form.to_dict()
            username = form_dict['username']
            email = form_dict['password']
            # Create table object to insert into db
            user = Users(username=username, email=email)
            # print out user details to console
            print(user.username, user.email, file=sys.stderr)
            # create a DB session and commit data
            db.session.add(user)
            db.session.commit()
            # db_helper.ins_usr()
            # store in session for future use
            session['username'] = username
            session['email'] = email
            g.email = email
            g.username = username
            print(g.username, g.email)
            # create mail object, frame acknowledgement message and send email
            msg = Message()
            msg.sender = props.MAIL_USERNAME
            msg.recipients = [email]
            msg.subject = "Request Acknowledgement"
            msg.body = "Request registered with email : " + email + " for " + username
            mail.send(msg)
            # redirect to app stack page
            return render_template("auth/appstack.html")
        except:
            return redirect("/auth/register")

    return render_template('auth/register.html')


@app.endpoint('appstack')
def appstack():
    print(session['username'])
    return render_template('auth/appstack.html')


@celery.task(name='FlaskApp.app.kickoff_analysis')
def kickoff_analysis(email):
    print("called salary run")
    if m.run_salary(app, g):
        print("salary run successfully completed")
        with open('globals.json', 'r') as fp:
            active_flags = json.load(fp)

        active_flags["appname"] = "salary"
        active_flags["mail"] = email
        active_flags["begin_upload"] = "TRUE"

        with open("globals.json", "w") as fp:
            json.dump(active_flags, fp)


@app.endpoint('thankyou')
def thankyou():
    if request.method == "POST":
        return redirect("/auth/register")
    email = session["email"]
    kickoff_analysis.delay(email)
    return render_template("Thankyou.html")


@app.endpoint('salary')
def salary():
    if request.method == "POST":
        try:

            uploaded_files = request.files.getlist("inputfile[]")
            print(uploaded_files)
            for file in uploaded_files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                csvfile = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')
                if filename[:-4] not in file_headers:
                    for row in csv.reader(csvfile, delimiter=","):
                        file_headers[filename[:-4]] = row
                        break
                print(file_headers)
                db_helper.push_to_db(str(os.path.join(app.config["UPLOAD_FOLDER"], filename)), filename)
            with open("headers.json", 'w') as file:
                json.dump(file_headers, file)
            msg = Message()
            msg.sender = "psourabh9218@gmail.com"
            email = session['email']
            msg.recipients = [email]
            msg.subject = "Files uploaded to Database Server"
            msg.body = "Files uploaded, request raised by   " + email + " complete. Generating results, This may take a few minutes"
            mail.send(msg)

            return redirect('/thankyou')

        except PermissionError:
            msg = Message()
            msg.sender = "psourabh9218@gmail.com"
            email = session['email']
            msg.recipients = [email]
            msg.subject = "Unable to write uploaded files to disk, Check for permissions on server"
            msg.body = "File save Error : " + email
            mail.send(msg)

    return render_template('apps/salary_pred.html')


# set mode
if __name__ == "__main__":
    app.run(debug=False)
