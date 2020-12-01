from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSController
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.clean import cleanup
import time
from multiprocessing.pool import ThreadPool as Pool

class TreeTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        # simple tree topology with depth 4 
        # 1 root host node (for server), 16 leaf host nodes
        # additional 14 host nodes can be attached to intermediate switches if required
        S = self.addHost("h1")
        L0_1 = self.addSwitch("s1")
        L1_1 = self.addSwitch("s2")
        # L1_1h = self.addSwitch("h2")
        L1_2 = self.addSwitch("s3")
        # L1_2h = self.addSwitch("h3")
        L2_1 = self.addSwitch("s4")
        # L2_1h = self.addSwitch("h4")
        L2_2 = self.addSwitch("s5")
        # L2_2h = self.addSwitch("h5")
        L2_3 = self.addSwitch("s6")
        # L2_3h = self.addSwitch("h6")
        L2_4 = self.addSwitch("s7")
        # L2_4h = self.addSwitch("h7")
        L3_1 = self.addSwitch("s8")
        # L3_1h = self.addSwitch("h8")
        L3_2 = self.addSwitch("s9")
        # L3_2h = self.addSwitch("h9")
        L3_3 = self.addSwitch("s10")
        # L3_3h = self.addSwitch("h10")
        L3_4 = self.addSwitch("s11")
        # L3_4h = self.addSwitch("h11")
        L3_5 = self.addSwitch("s12")
        # L3_5h = self.addSwitch("h12")
        L3_6 = self.addSwitch("s13")
        # L3_6h = self.addSwitch("h13")
        L3_7 = self.addSwitch("s14")
        # L3_7h = self.addSwitch("h14")
        L3_8 = self.addSwitch("s15")
        # L3_8h = self.addSwitch("h15")
        L4_1 = self.addSwitch("h16")
        L4_2 = self.addSwitch("h17")
        L4_3 = self.addSwitch("h18")
        L4_4 = self.addSwitch("h19")
        L4_5 = self.addSwitch("h20")
        L4_6 = self.addSwitch("h21")
        L4_7 = self.addSwitch("h22")
        L4_8 = self.addSwitch("h23")
        L4_9 = self.addSwitch("h16")
        L4_10 = self.addSwitch("h17")
        L4_11 = self.addSwitch("h18")
        L4_12 = self.addSwitch("h19")
        L4_13 = self.addSwitch("h20")
        L4_14 = self.addSwitch("h21")
        L4_15 = self.addSwitch("h22")
        L4_16 = self.addSwitch("h23")

        self.addLink(L3_1, L4_1, bw=100)
        self.addLink(L3_1, L4_2, bw=100)
        self.addLink(L3_2, L4_3, bw=100)
        self.addLink(L3_2, L4_4, bw=100)
        self.addLink(L3_3, L4_5, bw=100)
        self.addLink(L3_3, L4_6, bw=100)
        self.addLink(L3_4, L4_7, bw=100)
        self.addLink(L3_4, L4_8, bw=100)
        self.addLink(L3_5, L4_9, bw=100)
        self.addLink(L3_5, L4_10, bw=100)
        self.addLink(L3_6, L4_11, bw=100)
        self.addLink(L3_6, L4_12, bw=100)
        self.addLink(L3_7, L4_13, bw=100)
        self.addLink(L3_7, L4_14, bw=100)
        self.addLink(L3_8, L4_15, bw=100)
        self.addLink(L3_8, L4_16, bw=100)

        self.addLink(L2_1, L3_1, bw=200)
        self.addLink(L2_1, L3_2, bw=200)
        self.addLink(L2_2, L3_3, bw=200)
        self.addLink(L2_2, L3_4, bw=200)
        self.addLink(L2_3, L3_5, bw=200)
        self.addLink(L2_3, L3_6, bw=200)
        self.addLink(L2_4, L3_7, bw=200)
        self.addLink(L2_4, L3_8, bw=200)

        self.addLink(L1_1, L2_1, bw=400)
        self.addLink(L1_1, L2_2, bw=400)
        self.addLink(L1_2, L2_3, bw=400)
        self.addLink(L1_2, L2_4, bw=400)

        self.addLink(L0_1, L1_1, bw=800)
        self.addLink(L0_1, L1_2, bw=800)

        self.addLink(S, L0_1, bw=800)
        return

def xcute(inp):
    h = inp[0]
    i = inp[1]
    print("Exec", i)
    h[i].sendCmd("python client_" + str(i) +".py")
    return "Done"

if __name__ == "__main__":
    setLogLevel("info")
    topo = TreeTopo()

    net = Mininet(topo, link = TCLink, controller = OVSController)
    net.start()
    net.pingAll()
    
    net.hosts[0].sendCmd("python server.py")

    print("Starting")
    p = Pool(16)
    result = p.map(xcute, [[net.hosts, i] for i in range(1,17)])
    
    time.sleep(45)
    p.close()
    p.join()
    cleanup()
