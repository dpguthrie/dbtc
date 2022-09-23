RUN_COMMANDS = ['build', 'run', 'test', 'seed', 'snapshot']
GLOBAL_CLI_ARGS = {
    'warn_error': {'flags': ('--warn-error',), 'action': 'store_true'},
    'use_experimental_parser': {
        'flags': ('--use-experimental-parser',),
        'action': 'store_true',
    },
}
SUB_COMMAND_CLI_ARGS = {
    'vars': {'flags': ('--vars',)},
    'args': {'flags': ('--args',)},
    'fail_fast': {'flags': ('-x', '--fail-fast'), 'action': 'store_true'},
    'full_refresh': {'flags': ('--full-refresh',), 'action': 'store_true'},
    'store_failures': {'flags': ('--store-failures',), 'action': 'store_true'},
}
