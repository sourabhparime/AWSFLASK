from __init__ import *
import db_helper
from schema import *
from celery import Celery
from analysis import magic as m


# Frontend
@app.route("/")
def home():
    return redirect("auth/register")


@app.route("/auth/appstack", methods=["POST", "GET"])
def appstack():
    print(session['username'])
    return render_template('auth/appstack.html')


@celery.task(name='FlaskApp.app.kickoff_analysis')
def kickoff_analysis():
    print(m.run())


@app.route("/thankyou", methods=["POST", "GET"])
def thankyou():
    if request.method == "POST":
        return redirect("/auth/register")

    kickoff_analysis.delay()
    return render_template("Thankyou.html")


@app.route("/salary", methods=["POST", "GET"])
def salary():
    if request.method == "POST":
        try:
            # db_helper.clear_all_tables()
            uploaded_files = request.files.getlist("inputfile[]")
            print(uploaded_files)
            for file in uploaded_files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db_helper.push_to_db(str(os.path.join(app.config["UPLOAD_FOLDER"], filename)), filename)

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


@app.route("/auth/register", methods=["GET", "POST"])
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
            db_helper.ins_usr()
            # store in session for future use
            session['username'] = username
            session['email'] = email
            # create mail object, frame acknowledgement message and send email
            msg = Message()
            msg.sender = "psourabh9218@gmail.com"
            msg.recipients = [email]
            msg.subject = "Request Acknowledgement"
            msg.body = "Request registered with email : " + email + " for " + username
            mail.send(msg)
            # redirect to app stack page
            return redirect("auth/appstack")
        except:
            return redirect("/auth/register")

    return render_template('auth/register.html')


# set mode
if __name__ == "__main__":
    app.run(debug=True)
