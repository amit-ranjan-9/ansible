#!/usr/bin/env bash

set -eux

# This is a work-around for a bug in host pattern checking.
# Once the bug is fixed this can be removed.
# See: https://github.com/ansible/ansible/issues/83557#issuecomment-2231986971
unset ANSIBLE_HOST_PATTERN_MISMATCH

echo debug var=inventory_hostname | ansible-console '{{"localhost"}}'
# test environment variable setting with -E option
echo 'setup gather_subset=env' | ansible-console localhost -E 'TEST_CONSOLE_VAR=console_test_value' | grep '"TEST_CONSOLE_VAR": "console_test_value"'
