from bmtool import bmplot
import matplotlib.pyplot as plt

bmplot.connection_matrix(config="simulation_config_spikes_only.json",sources= "BLA", targets="BLA",
                                     sids="pop_name", tids="pop_name",no_prepend_pop=True, synaptic_info="1")



plt.show()