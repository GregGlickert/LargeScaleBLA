from neuron import h
import os

recordlist = []
def voltage_record(gids):
    global voltage, time
    try: 
        os.mkdir("voltage_reports")
    except:
        pass
    pc = h.ParallelContext()
    time = h.Vector().record(h._ref_t)
    for gid in gids:
        flag = pc.gid_exists(gid)
        if flag > 0 :
            filename = 'voltage_reports/voltage_report_gid_%d.txt'%gid
            cell = pc.gid2cell(gid)
            voltage = h.Vector()
            voltage.record(cell.soma[0](0.5)._ref_v)
            #voltage.label("soma %d" % (gid))
            recordlist.append((voltage, filename))
        else:
            pass

def save_voltage():
    for vmrec, filename in recordlist:
        f = open(filename, 'w')
        for j in range(int(vmrec.size())):
            f.write('%g %g\n'%(time.x[j], vmrec.x[j]))
        f.close()