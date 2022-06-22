from flask import Flask, request, flash, url_for, redirect, render_template  
from app.path  import add_nodes,add_edges,critical_path
from app import app
from app import db
from app.database import User,Nodes, Edges,Projects
from flask_login import login_user,login_required,current_user,logout_user

@app.route('/signup',methods=['GET','POST'])
def signup():
   if request.method == 'POST':
      user=User(request.form.get("InputUsername1"),request.form.get('InputPassword1'),request.form.get('InputEmail1'))
      db.session.add(user)  
      db.session.commit()  
      flash('Record was successfully added') 
      print("Added success")
      user_details()
      return redirect(url_for('details'))
   print("NOT POST")
   return render_template('sign.html') 

def user_details():
   users=User.query.all()
   for user in users:
      print("username: ",user.username,user.passwrd,user.email)

@app.route('/signin',methods=['GET','POST'])
def signin():
   user_details()
   if request.method == 'POST':
      e_mail=request.form.get("InputEmail2")
      print("email",e_mail)
      user=User.query.filter_by(email=e_mail).first()
      # print("Password",user.passwrd)
      if user is None:
         return redirect(url_for('signup'))
      pass_word=request.form.get("InputPassword2")
      print("Password",user.passwrd,pass_word)
      if user.passwrd==pass_word:
         print("Logged in successfully")
         login_user(user, remember=False)
         return redirect(url_for('details'))
   print("NOT POST")
   return render_template('home.html')

def clear_table():
   edges=Edges.query.all()
   for edge in edges:
      db.session.delete(edge)
   db.session.commit()

   nodes=Nodes.query.all()
   for node in nodes:
      db.session.delete(node)
   db.session.commit()

@app.route('/profile',methods=['GET','POST'])
@login_required
def details():
   print(current_user.username)
   if request.method=='POST':
      proj=Projects(request.form['projname'],request.form['projdescr'],current_user.id)
      db.session.add(proj)
      db.session.commit()
      clear_table()
      return redirect(url_for('addNode'))
   return render_template('profile.html',name=current_user.username)

# @app.route('/calculate')
# def cpm():
#    get_nodes()
#    flash('SUCCESS') 
#    return render_template('success.html')

@app.route('/addtask', methods = ['GET', 'POST'])
def addtsk():
   if request.method == 'POST':  
      node = Nodes(request.form['taskid'],request.form['taskdur'],request.form['taskdesc'])
      try:
         db.session.add(node)
         db.session.commit()
         return redirect('/addtask')
      except:
         return "Error adding to database"
   else:      
      return render_template('addtask.html',nodes = Nodes.query.all())


@app.route('/addedge',methods=['GET','POST'])
def addEdge():
   if request.method=='POST':
      node_is=request.form['edge']
      edges_are=request.form.getlist("edge_keys")
      node_id=Nodes.query.with_entities(Nodes.id).filter_by(nodename=node_is).first()
      for e in edges_are:
        edge=Edges(e,node_id[0])
        db.session.add(edge)
        db.session.commit()

      flash("Edges added successfully")
      return redirect(url_for('list_edges'))
   print("NOT POST")
   return render_template('add_edges.html',nodes=Nodes.query.all())

@app.route('/listedges')
def list_edges():
   return render_template('list_edges.html',edges=Edges.query.all())

@app.route('/delete',methods=['GET','POST'])
def del_node():
   if request.method=='POST':
      if not request.form['node_name']:
        flash('Please enter the name to delete','error')
      else:
         node_id=Nodes.query.with_entities(Nodes.id).filter_by(nodename=request.form['node_name']).first()  
         end_nodes=Edges.query.filter_by(edgename=request.form['node_name']).all() #delete the edges with end edge is node
         for n in end_nodes:
            db.session.delete(n)
         
         print("NODE_ID",node_id)

         if node_id is not None:
            start_nodes=Edges.query.filter_by(nodeid=node_id[0]).all() #delete the edges with start edge is node
            for n in start_nodes:
               db.session.delete(n)
         node=Nodes.query.filter_by(nodename=request.form['node_name']).first() #deleted the node from Nodes
         if node is not None:
            db.session.delete(node)
         db.session.commit()
         flash("Record was successfully deleted")
         return redirect(url_for('list_nodes'))
   return render_template('delete_node.html')

@app.route('/deleteedge',methods=['GET','POST'])
def del_edge():
   if request.method=='POST':
      if not request.form['start_node']:
        flash('Please enter the node1 to delete','error') 
      else:
         node_id=Nodes.query.with_entities(Nodes.id).filter_by(nodename=request.form['start_node']).first() 
         edge_id=Edges.query.filter_by(nodeid=node_id[0],edgename=request.form['end_node']).first()
         db.session.delete(edge_id)
         db.session.commit()
         flash("Record deleted successfully")
         return redirect(url_for('list_edges'))
   return render_template('delete_edge.html')

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('home.html'))

tasks=[]
dependencies=[]
crit_path=[]
result=[]

def get_nodes(result):
   nodes=Nodes.query.all()
   for node in nodes:
      add_nodes(tasks,node.nodename,node.duration)
   edges=Edges.query.all()
   for edge in edges:
      node1=Nodes.query.with_entities(Nodes.nodename).filter_by(id=edge.nodeid).first()
      add_edges(dependencies,node1[0],edge.edgename)
   result=critical_path(crit_path,dependencies,tasks)
   return result
res=[]
@app.route('/calculate')
def cpm():
   res=get_nodes(result)
   flash('SUCCESS') 
   print(res[0],res[1])
   return render_template('success.html',result=res)