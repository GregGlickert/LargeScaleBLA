from bmtk.analyzer.compartment import plot_traces
import h5py
import matplotlib.pyplot as plt

#fig1 = plot_traces(report_path='outputECP_NMDA/PN2PN_A_iampa.h5',node_ids=1424,show=False)
#fig2 = plot_traces(report_path='outputECP_NMDA/PN2PN_A_inmda.h5',node_ids=1424,show=False)
#fig3 = plot_traces(report_path='outputECP_NMDA/tone2PN_A_inmda.h5',node_ids=1424,show=False)
#fig4 = plot_traces(report_path='outputECP_NMDA/tone2PN_A_iampa.h5',node_ids=1424,show=False)
#fig5 = plot_traces(report_path='outputECP_NMDA/bg2PN_A_iampa.h5',node_ids=1424,show=False)
#fig6 = plot_traces(report_path='outputECP_NMDA/bg2PN_A_inmda.h5',node_ids=1424,show=False)

#plot_traces(report_path='outputECP_NMDA_test/v_report1.h5',show=False)
#plot_traces(report_path='outputECP_NMDA_test/v_report2.h5',show=False)
#plot_traces(report_path='outputECP_NMDA_test/v_report1.h5',show=False)
#plot_traces(report_path='outputECP_NMDA_test/PN2PN_A_iampa.h5',node_ids=1424,show=False)
#plot_traces(report_path='outputECP_NMDA_test/PN2PN_A_inmda.h5',node_ids=1424)
#plt.show()

f = h5py.File('outputECP_NMDA_test/PN2PN_A_inmda.h5')
data = (f['report']['BLA']['data'][:])

plt.plot(data)
plt.title('NMDA current')
plt.show()









