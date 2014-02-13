from xml.dom.minidom import parse
doc = parse('yql2.xml')
As = doc.getElementsByTagName("Answers")
f=open('out.txt','w')
for Answers in As:
    Aa = Answers.getElementsByTagName("Answer")
    for Answer in Aa:
        ANSWER = Answer.getElementsByTagName("Content")[0].childNodes[0].data
        #print >>f, ANSWER
        print ANSWER
    print 'done'
