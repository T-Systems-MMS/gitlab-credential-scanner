# Automated credential scanner

Background: We wanted to scan all our GitLab projects for leaked credentials. This way we want to improve our security standards company wide. This ReadMe explains how we use KICS to scan all repositories and how you can opt-out.

This repo runs a CI Job which scans all accessible repositories for credentials and creates a ticket with the scan result if there are any findings.

If you fixed the findings you can close the created issue and this job will automatically reopen and update the existing ticket if there are new issues found.

## Documentation

Please have a look at our official documentation: [https://github.com/T-Systems-MMS/gitlab-credential-scanner](https://github.com/T-Systems-MMS/gitlab-credential-scanner)

Note that we have a help function for all the available parameters. Currently this includes the following parameters:

```bash
usage: repo_scanner.py [-h] [--scan-repo SCAN_REPO] --gitlab-hostname
                       GITLAB_HOSTNAME --gitlab-access-token
                       GITLAB_ACCESS_TOKEN [--template-name TEMPLATE_NAME]
                       [--write-json-file WRITE_JSON_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --scan-repo SCAN_REPO
                        scan explicit repo with this name
  --gitlab-hostname GITLAB_HOSTNAME
                        hostname of gitlab (e.g. git.example.com)
  --gitlab-access-token GITLAB_ACCESS_TOKEN
                        access token for project or projects
  --template-name TEMPLATE_NAME
                        name of the template file used for the ticket
                        description
  --write-json-file WRITE_JSON_FILE
                        write statistics output in the named json file
```
## Contributing

If you want to contribute you can create a merge request so other colleagues will discuss the code with you. Make sure to add both a good and a bad practice to your code example.

## License

Copyright 2022-2023 T-Systems Multimedia Solutions GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Author Information
- Christopher Grau
- Sebastian Gumprich
- Christoph Sieber
- Henrik Hülle
- Andreas Hering
- Sebastian Bieger
- Daniel Uhlmann
