from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import *
from mininet.node import OVSController
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.clean import cleanup
import time
from multiprocessing.pool import ThreadPool as Pool


class CustomTopo_1( Topo ):
    def __init__(self):
        Topo.__init__(self)
        S = self.addHost("h1")
        A = self.addSwitch("s1")
        B = self.addSwitch("s2")
        C = self.addSwitch("s3")
        D = self.addSwitch("s4")
        E = self.addSwitch("s5")
        F = self.addSwitch("s6")
        G = self.addSwitch("s7")
        H = self.addHost("h8")
        I = self.addHost("h9")
        J = self.addHost("h10")
        K = self.addHost("h11")
        L = self.addHost("h12")
        M = self.addHost("h13")
        N = self.addHost("h14")
        O = self.addHost("h15")
        self.addLink(S, A, bw=400)
        self.addLink(A, B, bw=400)
        self.addLink(A, C, bw=400)
        self.addLink(B, D, bw=200)
        self.addLink(B, E, bw=200)
        self.addLink(C, F, bw=200)
        self.addLink(C, G, bw=200)
        self.addLink(D, H, bw=100)
        self.addLink(D, I, bw=100)
        self.addLink(E, J, bw=100)
        self.addLink(E, K, bw=100)
        self.addLink(F, L, bw=100)
        self.addLink(F, M, bw=100)
        self.addLink(G, N, bw=100)
        self.addLink(G, O, bw=100)

class CustomTopo_2( Topo ):
    def __init__(self):
        Topo.__init__(self)
        S = self.addHost("h1")
        A = self.addSwitch("s1")
        B = self.addSwitch("s2")
        C = self.addSwitch("s3")
        D = self.addSwitch("s4")
        E = self.addSwitch("s5")
        F = self.addSwitch("s6")
        G = self.addSwitch("s7")
        Sdash = self.addHost("h2")
        Sdashdash = self.addHost("h3")
        H = self.addHost("h8")
        I = self.addHost("h9")
        J = self.addHost("h10")
        K = self.addHost("h11")
        L = self.addHost("h12")
        M = self.addHost("h13")
        N = self.addHost("h14")
        O = self.addHost("h15")
        self.addLink(S, A, bw=400)
        self.addLink(A, B, bw=400)
        self.addLink(A, C, bw=400)
        self.addLink(B, D, bw=200)
        self.addLink(B, E, bw=200)
        self.addLink(C, F, bw=200)
        self.addLink(C, G, bw=200)
        self.addLink(D, H, bw=100)
        self.addLink(D, I, bw=100)
        self.addLink(E, J, bw=100)
        self.addLink(E, K, bw=100)
        self.addLink(F, L, bw=100)
        self.addLink(F, M, bw=100)
        self.addLink(G, N, bw=100)
        self.addLink(G, O, bw=100)

        self.addLink(F,Sdash, bw=400)
        self.addLink(G,Sdashdash, bw=400)
        self.addLink(B,C, bw=400)

def xecute(X):
    h = X[0]
    i = X[1]
    print("Exec", i)
    h[i].sendCmd("python3 client_" + str(i-1) +".py")
    return "Done"

if __name__ == "__main__":
    setLogLevel("info")
    # topo = SingleSwitchTopo(6)
    # topo = LinearTopo(k=1,n=2,bw = 100)
    # topo = CustomTopo_1()
    topo = CustomTopo_2()

    net = Mininet(topo,link = TCLink, controller = OVSController)
    net.start()
    net.pingAll()
    
    net.hosts[0].sendCmd("python3 tcp_server_1.py &")
    net.hosts[1].sendCmd("python3 tcp_server_2.py &")
    net.hosts[2].sendCmd("python3 tcp_server_3.py &")

    print("Starting")
    p = Pool(6)
    result = p.map(xecute, [[net.hosts, i] for i in [3,6,8,9]])
    # net.monitor(hosts=[h1],timeoutms=500)
    # CLI(net)
    
    time.sleep(45)
    p.close()
    p.join()
    cleanup()
