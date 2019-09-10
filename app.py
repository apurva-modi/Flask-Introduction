from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #setup application and is refrencing this file 
# 4 foward slashes means absolute path and 3 forward slashes means relative path.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# I am  using 3 forward slashes because I don't want to specify an exact location 
# I just want to reside in the project location.

#initialiszing the database.
db = SQLAlchemy(app)

class Todo(db.Model): #Creating a class model.
    id= db.Column(db.Integer, primary_key =True) 
    #id column that refrences the entry of each entry.
    content = db.Column(db.String(200),nullable=False)
    completed =db.Column(db.Integer, default=0)
    date_created= db.Column(db.DateTime,default=datetime.utcnow)

    # function to create a string everytime we create a new element.
    def __repr__(self):
    #everytime we create a new element it will return a new Task and the ID of that element created.
        return '<Task %r>' %self.id 


#  reate index route, so that when we browse to the URL we don't immediately get 404
# In flask we set up route using app route decorator.

@app.route('/', methods=['POST', 'GET']) 
#this route can accepts two methods now. 
#Instead of GET by default we can post to this route and send data to our database. 
def index():
    if request.method == 'POST':  #On submiting the form 
        task_content = request.form['content'] #requesting the form input content from the input field 'ID = content'
        new_task = Todo(content= task_content) #creating a model object for the class Todo 

        try:
            db.session.add(new_task) #will try to create a new task from the input
            db.session.commit() #will try to commit it to the database 
            return redirect('/') # will redirect us to the the index page 
        except:
            return 'There was an issue adding your Task'

    else:
        tasks =Todo.query.order_by(Todo.date_created).all() 
        # it will automatically look into templates folder. 
        return render_template('index.html',tasks = tasks) 

@app.route('/delete/<int:id>')
def delete(id):
    task2delete =Todo.query.get_or_404(id)
    try:
        db.session.delete(task2delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem in deleting the Task'

@app.route('/update/<int:id>',methods =['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method =='POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Unable to process the update sorry for the inconvinence'

    else:
        return render_template('update.html',task =task)



if __name__ =="__main__":
    app.run(debug=True)