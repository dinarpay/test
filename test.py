import sys, Queue, threading, os

class Apophis(threading.Thread):

    def __init__(self, queue, ports):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ports = ports
    def run(self):
        while True:
            host = self.queue.get()
            self.checker(host)
            self.queue.task_done()

    def checker(self, host):
        try:
            os.system('python MGK.py -p5060-6070,14310,9090,1025,1153,10243  %s %s' % (host, self.ports))
        except Exception as e:
            return False

def main(ips, ports, ThreadNmber):
    queue = Queue.Queue()
    for i in range(ThreadNmber):
        try:
            t = Apophis(queue, ports)
            t.daemon = True
            t.start()
        except Exception as e:
            break

    for Host in ips:
        queue.put(Host)

    queue.join()

if __name__ == '__main__':
    with open(sys.argv[1], 'rU') as ipf:
        ips = ipf.read().splitlines()
    
    ThreadNumber = sys.argv[2]
    
    ports = ""
    if len(sys.argv) == 4:
        ports = sys.argv[3];
    
    print 'Mohammad Elnwajha PRIV8T CODE'
    par = ''
    if par != '':
       print 'Exit'
    else:
        main(ips,  ports, int(ThreadNumber))
