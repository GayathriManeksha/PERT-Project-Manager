from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
   id=db.Column(db.Integer,primary_key=True)
   username=db.Column(db.String(20))
   passwrd=db.Column(db.String(20))
   email=db.Column(db.String(20))

   def __init__(self,username,passwrd,email):
      self.username=username
      self.passwrd=passwrd
      self.email=email

class Projects(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   proj_name=db.Column(db.String(10))
   proj_descr=db.Column(db.String(20))
   user_id=db.Column(db.Integer, db.ForeignKey(User.id))

   def __init__(self,proj_name,proj_descr,user_id):
      self.proj_name=proj_name
      self.proj_descr=proj_descr
      self.user_id=user_id

class Nodes(db.Model):  
   id = db.Column('id', db.Integer, primary_key = True)  
   nodename = db.Column(db.String(10))  
   task_descr=db.Column(db.String(20))
   duration = db.Column(db.Integer)
   proj_id=db.Column(db.Integer, db.ForeignKey(Projects.id))
  
   def __init__(self, nodename, duration,task_descr,proj_id):  
      self.nodename = nodename  
      self.duration = duration  
      self.task_descr=task_descr
      self.proj_id=proj_id
      
class Edges(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   # edgename=db.Column(db.String(10)) 
   nodeid2=db.Column(db.Integer, db.ForeignKey(Nodes.id))#endnode
   nodeid1=db.Column(db.Integer, db.ForeignKey(Nodes.id)) #startnode
   # nodes = relationship(Nodes, cascade = "all,delete", backref = "edges")

   def __init__(self,nodeid2,nodeid1):
      self.nodeid2=nodeid2
      self.nodeid1=nodeid1


