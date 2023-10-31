from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
client = MongoClient('mongodb://localhost:27017')
app.db = client.microblog

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        post_content = request.form['content']
        formatted_date = datetime.datetime.today().strftime('%d/%m/%Y')
        app.db.posts.insert_one({'content': post_content, 'date': formatted_date})
        return redirect(url_for('home'))
    entries_with_date = [
        (
        entry['content'],
        entry['date']
        ) for entry in app.db.posts.find({})
    ]
    return render_template('home.html', entries = entries_with_date)

if __name__ == '__main__':
    app.run(debug=True)