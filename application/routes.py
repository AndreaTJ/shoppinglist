from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, request
from application.forms import RegistrationForm, LoginForm, AddItems, CreateList
from application import app, db, bcrypt
from application.models import items, users, master,lists_
from sqlalchemy.sql import exists

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    if current_user.is_authenticated:
        form = CreateList()
        username=current_user.username
        alllists = lists_.query.filter(lists_.user_id == current_user.id).all()
        if form.validate_on_submit():

            listData = lists_(user_id = current_user.id,
            name = form.name.data)
                    
            db.session.add(listData)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print(form.errors)
        return render_template('home.html', title='Shopping list', list_=alllists,form=form,username=username)
    else:
        return redirect(url_for('register'))

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = users(username=form.username.data, password=hash_pw)
    
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html', title ='Register',form=form)

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update/<int:item_id>/<int:list_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id,list_id):
    master_item = master.query.filter(master.user_id == current_user.id, master.item_id == item_id, master.list_id == list_id).first()
    form = AddItems()
    if form.validate_on_submit():
        print(form.errors)
        db.session.delete(master_item)
        db.session.commit()
        if str(items.query.filter(items.name == form.name.data).all()) == '[]':
            itemsData = items(
                name = form.name.data,
                quantity = form.quantity.data,
                units = form.units.data
                )
            db.session.add(itemsData)
            db.session.commit()

        masterData = master(user_id = current_user.id,
        list_id = list_id,
        item_id = items.query.filter(items.name == form.name.data).first().id,
        name = form.name.data,
        quantity = form.quantity.data,
        units = form.units.data)
        db.session.add(masterData)
        db.session.commit()
        return redirect(url_for('lists',list_id = list_id))
    return render_template('update.html', title='Update', item=master_item, form=form)

@app.route('/delete/<int:item_id>/<int:list_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id,list_id):
    item = items.query.filter(items.id==item_id).first()
    master_item = master.query.filter(master.user_id == current_user.id, master.item_id == item_id, master.list_id == list_id).first()
    db.session.delete(master_item)
    db.session.commit()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('lists',list_id = list_id))

@app.route('/lists/<int:list_id>', methods=['GET','POST'])
@login_required
def lists(list_id):
    if current_user.is_authenticated:
        form = AddItems()
        username=current_user.username
        allitems = master.query.filter(master.user_id == current_user.id, master.list_id == list_id).all()
        if form.validate_on_submit():
            if str(items.query.filter(items.name == form.name.data).all()) == '[]':
                itemsData = items(
                    
                    name = form.name.data,
                    quantity = form.quantity.data,
                    units = form.units.data
                    )
                db.session.add(itemsData)
                db.session.commit()

            masterData = master(list_id = list_id,
            user_id = current_user.id,
            item_id = items.query.filter(items.name == form.name.data).first().id,
            name = form.name.data,
            quantity = form.quantity.data,
            units = form.units.data)

            db.session.add(masterData)
            db.session.commit()
            return redirect(url_for('lists',list_id = list_id))
        return render_template('lists.html', title='lists', list_=allitems,form=form,listname=lists_.query.filter(lists_.id == list_id).first())
'''
@app.route('/updatelist/<int:id>', methods=['GET', 'POST'])
@login_required
def update_list(id):
    list_id = id
    list_ = lists_.query.filter(lists_.id==id).first()
    form = CreateList()
    if form.validate_on_submit():
        print(form.errors)
        master_list = master.query.filter(master.user_id == current_user.id, master.list_id == list_id).all()
        db.session.delete(master_list)
        db.session.commit()
        if str(lists_.query.filter(lists_.name == form.name.data).all()) == '[]':
            listData = lists_(
                name = form.name.data,
                )
            db.session.add(listData)
            db.session.commit()

        masterData = master(user_id = current_user.id,
        list_id = lists_.query.filter(lists_.name == form.name.data).first().id,
        name = form.name.data,
        )
        db.session.add(masterData)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('updatelist.html', title='Update list',list_ = list_, form=form)
'''
@app.route('/deletelist/<int:list_id>', methods=['GET', 'POST'])
@login_required
def delete_list(list_id):
    list_ = lists_.query.filter(lists_.id==list_id).first()
    master_list = master.query.filter(master.user_id == current_user.id, master.list_id == list_id).all()
    if str(master_list) != '[]':
        if len(master_list) < 2:
            master_list = master.query.filter(master.user_id == current_user.id, master.list_id == list_id).one()        
        db.session.delete(master_list)
        db.session.commit()
    db.session.delete(list_)
    db.session.commit()
    return redirect(url_for('home'))   
