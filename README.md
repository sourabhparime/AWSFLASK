# Data Science Deployed
<p>An extensible end-to-end data science solution created using Flask, Celery, SQL ALchemy and Rabbit MQ , deployed on AMAZON EC2 and Microsoft server instances</p><br>
<p>Applications currently served: </p>
<ol> 1. Salary Prediction System </p></ol>

<p><h2>Configuration on local development environment</h2></p>
<ol>1. Check out the project and install dependencies from the requirements.txt </ol>
<ol>2. Register the app on google drive API (to upload the results) and save teh credentials in the app folder.</ol>
<ol>3. Edit the template files and save them without .template extension. </ol>
<ol>4. You can use any message broker and backend data base, edit the URI's accordingly. </ol>
<ol>5. Run authenticate.py to check for Google Drive connectivity. </ol>
<ol>6. Open a terminal and run upload_results.py</ol>
<ol>7. Open another terminal and start celery broker using teh command celery worker -A app.celery --pool=eventlet --loglevel=info. </ol>
<ol>8. Finally run the flask app.</ol><br>

<p>Data set can be downloaded from https://drive.google.com/drive/folders/1mJcUpmtPWAe7NlM6UUqe8lkpmFGw_V08?usp=sharing. <br>
This application can be extended to any number of use cases, just add the URL in application stack page and route it like salary app  </p>

<p>Demo<br>
[embed]https://github.com/sourabhparime/AWSFLASK/blob/master/DATA%20SCIENCE%20DEPLOYED.pdf[/embed]
</p>
