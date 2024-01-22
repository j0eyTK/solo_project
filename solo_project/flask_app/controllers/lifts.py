from flask import Flask, render_template, session, redirect, flash, request
from flask_app import app

from flask_app.models.user import User

from flask_app.models.lift import Lift

@app.route('/lifts/create')
def create_lift():

    if not 'user_id' in session:
        return redirect('/')

    data = {
        "id": session["user_id"]
    }
    return render_template('create.html', user=User.get_by_one(data))




@app.route('/lifts/<lift_id>')
def description(lift_id):
    lift = Lift.get_one_by_id(lift_id)
    if not lift:
        return redirect('/dashboard')
    
    user_id = session.get('user_id')
    user = User.get_by_one({'id':user_id})

    return render_template ('view.html', lift=lift, user=user)


@app.route('/lifts/delete/<lift_id>')
def delete_lift(lift_id):

    Lift.delete_by_id(lift_id)

    return redirect ('/dashboard')


@app.route('/lifts/edit/<lift_id>')
def edit_lift(lift_id):

    if not 'user_id' in session:
        return redirect('/')

    return render_template ('edit.html',lift = Lift.get_one_by_id(lift_id))


@app.route('/lifts/create', methods = ['POST'])
def add_lift():

    if not 'user_id' in session:
        return redirect('/')
    
    is_valid = Lift.validate_lift(request.form)

    if is_valid:
        Lift.save(request.form)
        return redirect ('/dashboard')
    
    else:
        return redirect('/lifts/create')
    

@app.route('/lifts/update', methods = ['POST'])
def update_lift():

    if not 'user_id' in session:
        return redirect('/')
    
    
    form_data = dict(request.form)
    data = {
        'id':form_data['id'],
        'name':form_data['name'],
        'age':form_data['age'],
        'lift':form_data['lift'],
        'weight':form_data['weight'],
        
    }   

    Lift.update(data)
    return redirect('/dashboard')