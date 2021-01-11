import mgen

receiver = mgen.Controller("receiver")

receiver.send_event("listen udp 5000")

updateCount = 1
for line in receiver:
    event = mgen.Event(line)
    # print the line received
    print line,
    # print payload content, if applicable
    if event.data:
        print "   (payload content is \"%s\")" % event.data