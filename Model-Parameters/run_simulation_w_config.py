import yaml
import json
from pathlib import Path
import shutil
import os
from bmtool.SLURM import SimulationBlock, BlockRunner, seedSweep, multiSeedSweep

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_directories(config):
    """Setup output directories."""
    base_path = Path.cwd()
    target_dir = (base_path / config['simulation']['output_name']).resolve() 
    
    if target_dir.exists() and target_dir.is_dir():
        shutil.rmtree(target_dir)
    
    return base_path, target_dir

def check_ecp_module(config, coreneuron_flag):
    """Force the ecp recording module to be either extracellular for regular bmtk neuron sims
    and ecp for the corebmtk and coreneuron sims.
    """
    print(f"Editing {config} guessing that the report is config['reports']['ecp']")
    with open(config, 'r') as sim_config:
        sim_dict = json.load(sim_config)
        if coreneuron_flag == 'True':
            sim_dict['reports']['ecp']['module'] = 'ecp'
        else:
            sim_dict['reports']['ecp']['module'] = 'extracellular'
    
    with open(config, 'w') as f:
        json.dump(sim_dict, f, indent=4,
                  ensure_ascii=False, sort_keys=False)    

def create_simulation_cases(config, use_coreneuron):
    """Create simulation cases dictionary."""
    cases = {}
    coreneuron_flag = "True" if use_coreneuron else "False"
    
    for case_name, case_config in config['simulation_cases'].items():
        check_ecp_module(case_config['config_file'], coreneuron_flag)
        if use_coreneuron:
            command = f"mpirun ./components/mechanisms/x86_64/special -mpi -python run_network.py {case_config['config_file']} {coreneuron_flag}"
        else:
            command = f"mpirun nrniv -mpi -python run_network.py {case_config['config_file']} {coreneuron_flag}"
        cases[case_name] = command
    
    return cases

def generate_param_values(sweep_config):
    """Generate parameter values based on sweep configuration.
    
    This function handles both absolute values and percentage-based changes.
    """
    if 'value' in sweep_config['sweep_method']:
        # Use absolute values directly
        return sweep_config['param_values']
    elif 'percentage' in sweep_config['sweep_method']:
        # Calculate values based on percentage change
        base_value = sweep_config.get('base_value', 1.0)
        percent = sweep_config['percent_change']
        iterations = sweep_config.get('iterations', 5)
        
        values = [base_value]
        current_value = base_value
        
        for _ in range(iterations):
            current_value = current_value * (1 + percent/100)
            values.append(round(current_value, 2))
            
        return values
    else:
        # Default to a single value if neither is specified
        raise Exception("Invalid sweep method")
        return [1]

# Load configuration
config = load_config(config_path='slurm-config-setup.yaml')

# Setup basic parameters
base_path, target_dir = setup_directories(config)
env = config['simulation']['environment']
slurm_config = config['slurm'][env]

# Create simulation cases
simulation_cases = create_simulation_cases(
    config, 
    config['simulation']['use_coreneuron']
)

# Setup block parameters
block_params = {
    'time': slurm_config['time'],
    'partition': slurm_config['partition'],
    'nodes': slurm_config['nodes'],
    'ntasks': slurm_config['ntasks'],
    'mem': slurm_config['mem'],
    'output_base_dir': str(target_dir),
}

if 'account' in slurm_config:
    block_params['account'] = slurm_config['account']

# Determine parameter values based on sweep configuration
if config['simulation']['seed_sweep'] != 'none':
    param_values = generate_param_values(config['sweep_config'])
    num_blocks = len(param_values)
else:
    param_values = [1]  # just a temp value for the length of 1
    num_blocks = 1

# Create blocks
blocks = []
for i in range(1, num_blocks + 1):
    block_name = f'block{i}'
    block = SimulationBlock(block_name, **block_params, 
                            simulation_cases=simulation_cases,
                            additional_commands=config['module_commands'][env],
                            component_path=config['simulation']['component_path'])
    blocks.append(block)

# Create runner parameters
runner_params = {
    'blocks': blocks,
    'webhook': config['simulation']['webhook_url'],
}

# if json_editor is there then it's either seed or multi
if config['simulation']['seed_sweep'] != 'none':
    runner_params.update({
        'json_file_path': config['sweep_config']['base_json_file'],
        'param_name': config['sweep_config']['param_name'],
        'param_values': param_values})
    
    if config['simulation']['seed_sweep'] == 'multiseed':
        for related_file in config['sweep_config'].get('multiseed_files', []):
            syn_dict = {
                'json_file_path': related_file['path'],
                'ratio': related_file['ratio']}
        runner_params.update({
            'syn_dict': syn_dict
        })

runner = BlockRunner(**runner_params)

# Submit blocks according to configuration
if config['simulation'].get('parallel_submission', False) and num_blocks > 1:  # length of 1 can just use sequentially
    runner.submit_blocks_parallel()
else:
    runner.submit_blocks_sequentially()