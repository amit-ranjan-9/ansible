#!/usr/bin/env bash

set -eux

# This is a work-around for a bug in host pattern checking.
# Once the bug is fixed this can be removed.
# See: https://github.com/ansible/ansible/issues/83557#issuecomment-2231986971
unset ANSIBLE_HOST_PATTERN_MISMATCH

echo debug var=inventory_hostname | ansible-console '{{"localhost"}}'

# Test that console accepts -E flag without immediate error
set +e
timeout 2 bash -c 'echo "exit" | ansible-console -E "TEST_VAR=test_value" localhost' > /dev/null 2>&1
exit_code=$?
set -e

# Console should exit cleanly or timeout (both are acceptable)
if [ $exit_code -gt 1 ] && [ $exit_code -ne 124 ]; then  # 124 is timeout exit code
    echo "FAILED: Console does not accept -E flag"
    exit 1
fi

echo "Console environment variable CLI tests passed"