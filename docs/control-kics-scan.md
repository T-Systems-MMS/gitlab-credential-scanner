# Exclude files and paths from scanning

If you get false positives you can exclude certain files or directories from scanning by adding
a kics.config file to your repositories root directory.

Note: KICS supports JSON, TOML, YAML, and HCL formats for the configuration files, and it is able to infer the formats without the need of file extension.

For more configuration options, please see: https://docs.kics.io/latest/configuration-file/

## Example Configuration

```yaml
---
# exclude external components which might include example passwords
exclude-paths:
  - "ansible/collections/"
  - "ansible/roles/external"
```
# Exclude lines from scanning

If you want to exclude a specific line from our scanning you write `# kics-scan ignore-line` and it will ignore the following line.

```yaml
1: resource "google_storage_bucket" "example" {
2:  # kics-scan ignore-line
3:  name          = "image-store.com"
4:  location      = "EU"
5:  force_destroy = true
6: }
```
Results that point to lines 2 and 3 will be ignored.

For a more detailed overview have a look at: https://docs.kics.io/latest/running-kics/#using_commands_on_scanned_files_as_comments
