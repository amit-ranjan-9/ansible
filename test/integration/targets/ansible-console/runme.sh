#!/usr/bin/env bash

set -eux

# This is a work-around for a bug in host pattern checking.
# Once the bug is fixed this can be removed.
# See: https://github.com/ansible/ansible/issues/83557#issuecomment-2231986971
unset ANSIBLE_HOST_PATTERN_MISMATCH

echo debug var=inventory_hostname | ansible-console '{{"localhost"}}'
# test environment variable setting with -E option (basic KEY=VALUE)
echo 'setup gather_subset=env' | ansible-console localhost -E 'TEST_CONSOLE_VAR=console_test_value' | grep '"TEST_CONSOLE_VAR": "console_test_value"'

# test environment variable setting with -E option (file format)
cat > /tmp/console_env_file.yml << 'EOF'
TEST_CONSOLE_FILE_VAR: console_file_value
EOF
echo 'setup gather_subset=env' | ansible-console localhost -E '@/tmp/console_env_file.yml' | grep '"TEST_CONSOLE_FILE_VAR": "console_file_value"'

# test environment variable setting with -E option (JSON format)
echo 'setup gather_subset=env' | ansible-console localhost -E '{"TEST_CONSOLE_JSON": "console_json_value"}' | grep '"TEST_CONSOLE_JSON": "console_json_value"'
