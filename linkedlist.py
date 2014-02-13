#LINKED LIST FOR SIMILAR CLUSETRS
class Clusternode:
    def __init__(self):
       # self.data = data
        self.next = None
        self.child=None

class Sentencenode:
    def __init__(self, data,pos):
        self.data = data
        self.pos = pos
        self.next = None
        
 
class LinkedList :
    def __init__( self ) :
        self.head = None        
 
    def add( self, data,pos ) :
        node = Clusternode()
        snode=Sentencenode(data,pos)
        if (self.head == None):
                    node.next=None
                    node.child=snode
                    self.head = node
            
        else :
                        tnode=self.head
                        while(tnode.next!=None):
                            tnode=tnode.next
                        tnode.next=node
                        node.next=None
                        node.child=snode
       # print(data)

    def addsen(self,data,pos,clust):
            snode=Sentencenode(data,pos)
            tsnode=clust.child
            while(tsnode.next!=None):
                tsnode=tsnode.next          #later add the sentence cluster according to the rank
            tsnode.next=snode
            
 
    def search( self, k ) :
        p = self.head
        if p != None :
            while p.next != None :
                if ( p.child.data == k ) :
                    return p                
                p = p.next
            if ( p.child.data == k ) :
                return p
        return None
 

    def getSent(self,clust):
        return clust.child.data

    def display(self):
        temp=self.head
        while(temp!=None):
            temp1=temp.child
            while(temp1!=None):
                print(temp1.data)
                temp1=temp1.next
            print("\n")
            temp=temp.next
