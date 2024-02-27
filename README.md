# Graph-Email-Dumper
Script to dump emails through Microsoft Graph API

# Usage

```
python3 graph_dump.py extended_azure_token_file_path (optional filter)
```
# Filter examples

```
'$search="body:password"'
'$search="attachment:password"'
'$search="attachment:password"'

python3 graph_dump.py extended_azure_token_file_path '$search="body:password"'
```

# Credit
Mr.Un1k0d3r RingZer0 Team
