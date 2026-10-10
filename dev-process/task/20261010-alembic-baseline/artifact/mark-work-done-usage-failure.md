# mark-work-done usage failure

- First error: `mark-work-done: error: the following arguments are required: --summary`.
- The command exited during argument parsing and did not mutate task completion state.
- `mark-work-done --help` confirms that `--summary SUMMARY` is mandatory.
