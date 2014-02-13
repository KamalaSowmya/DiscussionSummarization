class Themenode:
    def __init__(self):
        self.name = None
        self.next = None
        self.child = None

class ThemeSentencenode:
    def __init__(self, data,pos):
        self.data = data
        self.pos = pos
        self.next = None


class ThemeLinkedList :
    def __init__( self ) :
        self.head = None

    def add( self,themename,data,pos) :
        node = Themenode()
        snode=ThemeSentencenode(data,pos)
        if (self.head == None):
                    node.next=None
                    node.child=snode
                    node.name=themename
                    self.head = node

        else :
                        tnode=self.head
                        while(tnode.next!=None):
                            tnode=tnode.next
                        tnode.next=node
                        node.next=None
                        node.child=snode
                        node.name=themename
       # print(data)

    def addsen(self,data,pos,clust):
            snode=ThemeSentencenode(data,pos)
            tsnode=clust.child
            while(tsnode.next!=None):
                tsnode=tsnode.next          #later add the sentence cluster according to the rank
            tsnode.next=snode

 #returning the cluster : k = name of the cluster, else returns none
    def search( self, k ) :
        p = self.head
        if p != None :
            while p.next != None :
                if ( p.name == k ) :
                    return p
                p = p.next
            if ( p.name == k ) :
                return p
        return None

    def retrieveSen(self,clust):
        sen=[]
        p=clust.child
        while(p!=None):
            sen.append(p.data)
            p=p.next
        return sen

    def retrievePos(self,clust):
        position=[]
        p=clust.child
        while(p!=None):
            position.append(p.pos)
            p=p.next
        return position



    def getSent(self,clust):
        return clust.child.data

    def display(self):
        temp=self.head
        while(temp!=None):
            print temp.name
            temp1=temp.child
            while(temp1!=None):
                print(temp1.data)
                temp1=temp1.next
            print("\n       *********************************")
            temp=temp.next
