from bmtool.SLURM import SimulationBlock, BlockRunner

# 
on_Expanse = False
on_HellBender = False
output_name = "????" 
flow_url="https://prod-36.westus.logic.azure.com:443/workflows/5e3bbadcc1174484993676e5a5b02264/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9a6oJfV7LnbdlhEoofo1nfoR4W4zuT1feBhf2N6hG1k"

# Define simulation cases
# simulation_cases (dict): Dictionary of simulation cases and their corresponding commands.
simulation_cases = {
    "baseline": "mpirun nrniv -quiet -mpi -python run_network.py simulation_configECP_baseline_homogenous.json",
    #"trials": "mpirun nrniv -quiet -mpi -python run_network.py simulation_configECP_trials_homogenous.json",
    #"tone+shock": "mpirun nrniv -mpi -quiet -python run_network.py simulation_configECP_tone+shock_homogenous.json"
}

# Define block parameters
# could add other params like account to allow working on Expanse
if on_Expanse:
    block_params = {
        'time': '02:30:00',
        'partition': 'shared',
        'nodes': 1,
        'ntasks': 40,
        'mem': 160,
        'output_base_dir': f'../Run-Storage/{output_name}',
        'account':'umc113'
    }
elif on_HellBender:
    block_params = {
        'time': '02:30:00',
        'partition': 'general',
        'nodes': 1,
        'ntasks': 30,
        'mem': 120,
        'output_base_dir': f'../Run-Storage/{output_name}',
    }
else:
    block_params = {
    'time': '04:00:00',
    'partition': 'batch',
    'nodes': 1,
    'ntasks': 10,
    'mem': 20,
    'output_base_dir': f'../Run-Storage/{output_name}',
    'account':'kac2cf'
    }


# Define the number of blocks to create
num_blocks = 1

# Create a list to hold the blocks
blocks = []

# commands you want to run in the script before bmtk starts useful for HPCs
if on_Expanse:
    additional_commands = [
        "module purge",
        "module load slurm",
        "module load cpu/0.17.3b",
        "module load gcc/10.2.0/npcyll4",
        "module load openmpi/4.1.1",
        "export HDF5_USE_FILE_LOCKING=FALSE"
    ]
elif on_HellBender:
    additional_commands = [
        'module load intel_mpi']

else:
    additional_commands = [
        'module load mpich-x86_64-nopy']

# Create blocks with the defined simulation cases
for i in range(1, num_blocks + 1):
    block_name = f'block{i}'
    block = SimulationBlock(block_name, **block_params, simulation_cases=simulation_cases,additional_commands=additional_commands,
                            status_list = ['COMPLETED', 'RUNNING'])
    blocks.append(block)


# Create a SequentialBlockRunner with the blocks and parameter changes
runner = BlockRunner(blocks,check_interval=20,webhook=flow_url)

# Submit the blocks sequentially
runner.submit_blocks_sequentially()