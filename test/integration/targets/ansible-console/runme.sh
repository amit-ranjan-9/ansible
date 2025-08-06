#!/usr/bin/env bash

set -eux

# This is a work-around for a bug in host pattern checking.
# Once the bug is fixed this can be removed.
# See: https://github.com/ansible/ansible/issues/83557#issuecomment-2231986971
unset ANSIBLE_HOST_PATTERN_MISMATCH

echo debug var=inventory_hostname | ansible-console '{{"localhost"}}'
# test environment variable setting with -E option
echo 'setup' | ansible-console localhost -E 'TEST_ENV_VAR=ansible_console_test_value' | grep 'TEST_ENV_VAR'
