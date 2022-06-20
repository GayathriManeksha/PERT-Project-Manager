from app import db

class Nodes(db.Model):  
   id = db.Column('id', db.Integer, primary_key = True)  
   nodename = db.Column(db.String(10))  
   duration = db.Column(db.Integer)
  
   def __init__(self, nodename, duration):  
      self.nodename = nodename  
      self.duration = duration  
      
class Edges(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   edgename=db.Column(db.String(10)) #endnode
   nodeid=db.Column(db.Integer, db.ForeignKey(Nodes.id)) #startnode
   # nodes = relationship(Nodes, cascade = "all,delete", backref = "edges")

   def __init__(self,edgename,nodeid):
      self.edgename=edgename
      self.nodeid=nodeid