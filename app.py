from flask import Flask, render_template, url_for, flash, request, send_file, jsonify
import os
import redis
from rq import Queue
from rq.job import Job
from worker import conn
from lb_processing import cloud_processing


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12345')

q = Queue(connection=conn, default_timeout=1800)


@app.route("/", methods=['GET', 'POST'])
def home():
	image_file = None
	return render_template("home.html", image_file=image_file)


@app.route("/get-cloud", methods=['POST'])
def get_cloud():
	username = request.form['username']
	if username:
		job = q.enqueue(cloud_processing, username)
		return jsonify({}), 202, {'Location': url_for('job_status', job_id=job.get_id())}
	return jsonify({'error': 'You need to input a username.'})


@app.route("/status/<job_id>", methods=['GET'])
def job_status(job_id):
    job = q.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknown'}
    elif job.result is False:
    	response = {'status': 'invalid'}
    else:
        response = {
            'status': job.get_status(),
            'image': job.result,
        }
        # if job.is_failed:
            # response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=(os.environ.get('DEBUG_VALUE') == 'True'))