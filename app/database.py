from app import db

class Nodes(db.Model):  
   id = db.Column('id', db.Integer, primary_key = True)  
   nodename = db.Column(db.String(10))  
   task_descr=db.Column(db.String(20))
   duration = db.Column(db.Integer)
  
   def __init__(self, nodename, duration,task_descr):  
      self.nodename = nodename  
      self.duration = duration  
      self.task_descr=task_descr
      
class Edges(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   edgename=db.Column(db.String(10)) #endnode
   nodeid=db.Column(db.Integer, db.ForeignKey(Nodes.id)) #startnode
   # nodes = relationship(Nodes, cascade = "all,delete", backref = "edges")

   def __init__(self,edgename,nodeid):
      self.edgename=edgename
      self.nodeid=nodeid

class User(db.Model):
   id=db.Column(db.Integer,primary_key=True)
   username=db.Column(db.String(20))
   passwrd=db.Column(db.String(20))
   email=db.Column(db.String(20))

   def __init__(self,username,passwrd,email):
      self.username=username
      self.passwrd=passwrd
      self.email=email