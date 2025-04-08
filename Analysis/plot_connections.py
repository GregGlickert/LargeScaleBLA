from bmtool import bmplot
import matplotlib.pyplot as plt

#bmplot.connection_matrix(config="simulation_configECP_base_homogenous.json",sources= "BLA", targets="BLA",
#                                     sids="pop_name", tids="pop_name",no_prepend_pop=True, synaptic_info="1")

bmplot.convergence_connection_matrix(config="simulation_configECP_base_homogenous.json",sources= "all", targets="all")
plt.show()