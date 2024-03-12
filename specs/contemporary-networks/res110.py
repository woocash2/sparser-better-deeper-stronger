from main import parse_args_default
from data_handling.utils import combine_with_defaults
from mrunner.helpers.specification_helper import create_experiments_helper

name = globals()["script"][:-3]

base_config = {
    "batch_size": 128,
    "test_batch_size": 128,
    "multiplier": 1,
    "epochs": 200,
    "lr": 0.1,
    "seed": 17,
    "optimizer": "sgd",
    "data": "cifar10",
    "model" : 'cifar_resnet_56',
    "l2": 1.0e-4,
    'bench': False,
    'scaled': False,
    'sparse': True,
    'fix': False,
    'sparse_init': 'erk',
    'growth': 'random',
    'death': 'magnitude',
    'redistribution': 'none',
    'death_rate': 0.0,
    'density': 0.05,
    'update_frequency': 100,
    'decay_schedule': 'cosine',
    'use_wandb': False,
    'save_locally': False,
    'tag': name,
    'sigma_w': 1.00,
    'sigma_b': 0.0,
    'q_star': 1,
    "activation": 'relu',
    'depth': 7,
    'width': 100,
    'no_cuda': False,
    'record_jacobian': False,
    'more_nonzeros': True,
}

base_config = combine_with_defaults(
    base_config, defaults=vars(parse_args_default([]))
)


params_grid = [
    { # Dense ResNet baseline
        "seed": [1, 2, 3, 4, 5],
        "model" : ['cifar_resnet_110'],
        "density": [1.0],
        "scaled": [False],
        "fix": [True],
        "sparse": [False],
        "init_type": ['conv_orthogonal', 'default'],
        'activation': ['relu'],
    },
    { # Sparse baselines
        "seed": [1, 2, 3, 4, 5],
        "model" : ['cifar_resnet_110'],
        "density": [0.05, 0.1],
        "scaled": [False],
        "fix": [True],
        "sparse": [True],
        "init_type": ['conv_orthogonal'],
        'sparse_init': ['uniform', 'erk', 'snip_direct', 'grasp_direct', 'uniform_AI', 'erk_AI', 'snip_direct_AI', 'grasp_direct_AI'],
        'activation': ['relu'],
    },
    { # Our ResNet
        "seed": [1, 2, 3, 4, 5],
        "model" : ['cifar_resnet_110'],
        "density": [0.05, 0.1],
        "scaled": [False],
        "fix": [True],
        "sparse": [True],
        "init_type": ['conv_orthogonal'],
        'sparse_init': ['uniform_EI', 'erk_EI', 'snip_direct_EI', 'grasp_direct_EI'],
        'activation': ['relu'],
        'lr': [0.1, 0.01],
    },
    { # Synflow double precision
        "seed": [1, 2, 3, 4, 5],
        "model" : ['cifar_resnet_110'],
        "density": [0.05, 0.1],
        "scaled": [False],
        "fix": [True],
        "sparse": [True],
        "init_type": ['conv_orthogonal'],
        'sparse_init': ['synflow_direct',  'synflow_direct_AI', 'synflow_direct_EI'],
        'activation': ['relu'],
        'double_precision': [True]
    },
]

experiments_list = create_experiments_helper(
    experiment_name=name,
    project_name="ortho",
    script="python mrun.py",
    python_path="",
    exclude=[
        ".pytest_cache",
        "__pycache__",
        "checkpoints",
        "out",
        "singularity",
        ".vagrant",
        "notebooks",
        "Vagrantfile",
        "results",
        "download"
    ],
    tags=[name],
    base_config=base_config,
    params_grid=params_grid,
)