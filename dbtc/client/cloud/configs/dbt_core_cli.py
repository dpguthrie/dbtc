run_commands = ['build', 'run', 'test', 'seed', 'snapshot']

global_cli_args = {
    'warn_error': {'flags': ('--warn-error',), 'action': 'store_true'},
    'use_experimental_parser': {
        'flags': ('--use-experimental-parser',),
        'action': 'store_true',
    },
}

sub_command_cli_args = {
    'vars': {'flags': ('--vars',)},
    'args': {'flags': ('--args',)},
    'fail_fast': {'flags': ('-x', '--fail-fast'), 'action': 'store_true'},
    'full_refresh': {'flags': ('--full-refresh',), 'action': 'store_true'},
    'store_failures': {'flags': ('--store-failures',), 'action': 'store_true'},
}
