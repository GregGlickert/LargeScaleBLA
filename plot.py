from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot


raster = plot_raster(config_file='simulation_config.json', group_by='pop_name', title="raster")
rates = plot_rates_boxplot(config_file='simulation_config.json', group_by='pop_name')
