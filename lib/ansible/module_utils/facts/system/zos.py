from __future__ import annotations

from ansible.module_utils.facts.collector import BaseFactCollector


class ZOSFactCollector(BaseFactCollector):
    name = 'zos'
    _fact_ids = set([
        'date_time',
        'uptime_seconds',
        'mounts',
        'userspace_architecture',
        'distribution',
    ])

    def collect(self, module=None, collected_facts=None):
        zos_facts = {}
        
        # Only run on z/OS or OS/390 platforms
        platform_system = collected_facts.get('platform', {}).get('system', '')
        if platform_system != 'z/OS' and platform_system != 'OS/390':
            # Try to detect if we're on z/OS by examining commands
            uname_cmd = module.run_command('uname -s')
            if uname_cmd[0] != 0 or ('OS/390' not in uname_cmd[1] and 'Z/OS' not in uname_cmd[1].upper()):
                return zos_facts
            
        # Collect date_time
        date_time_cmd = module.run_command('date "+%Y-%m-%d %H:%M:%S %Z"')
        if date_time_cmd[0] == 0:
            zos_facts['date_time'] = date_time_cmd[1].strip()
        
        # Collect uptime_seconds 
        # Using 'ps -o etime= -p 1' to get elapsed time of init process
        uptime_cmd = module.run_command('ps -o etime= -p 1')
        if uptime_cmd[0] == 0:
            uptime_str = uptime_cmd[1].strip()
            # Parse the elapsed time format (days-hours:minutes:seconds)
            uptime_seconds = 0
            
            if '-' in uptime_str:  # Format: days-hours:minutes:seconds
                days, rest = uptime_str.split('-', 1)
                uptime_seconds += int(days) * 86400  # days to seconds
                uptime_str = rest
                
            time_parts = uptime_str.split(':')
            if len(time_parts) == 3:  # Format: hours:minutes:seconds
                uptime_seconds += int(time_parts[0]) * 3600  # hours to seconds
                uptime_seconds += int(time_parts[1]) * 60    # minutes to seconds
                uptime_seconds += int(time_parts[2])         # seconds
            elif len(time_parts) == 2:  # Format: minutes:seconds
                uptime_seconds += int(time_parts[0]) * 60    # minutes to seconds
                uptime_seconds += int(time_parts[1])         # seconds
                
            zos_facts['uptime_seconds'] = uptime_seconds
        
        # Collect mounts
        mount_cmd = module.run_command('df -P')
        if mount_cmd[0] == 0:
            zos_facts['mounts'] = []
            mount_lines = mount_cmd[1].strip().split('\n')[1:]  # Skip header
            for line in mount_lines:
                parts = line.split()
                if len(parts) >= 6:
                    mount_info = {
                        'device': parts[0],
                        'size_total': int(parts[1]) * 1024,  # Convert to bytes
                        'size_available': int(parts[3]) * 1024,  # Convert to bytes
                        'mount': parts[5]
                    }
                    zos_facts['mounts'].append(mount_info)
        
        # Collect userspace_architecture
        arch_cmd = module.run_command('uname -m')
        if arch_cmd[0] == 0:
            zos_facts['userspace_architecture'] = arch_cmd[1].strip()
        
        # Collect distribution info
        zos_facts['distribution'] = "z/OS"
        
        # Try to get the z/OS version
        version_cmd = module.run_command('uname -v')
        if version_cmd[0] == 0:
            zos_facts['distribution_version'] = version_cmd[1].strip()
        
        release_cmd = module.run_command('uname -r')
        if release_cmd[0] == 0:
            zos_facts['distribution_release'] = release_cmd[1].strip()
            
        return zos_facts