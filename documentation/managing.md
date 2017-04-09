# Managing your SiteFab installation

## Upgrading SiteFab

Here is how to upgrade SiteFab:

1. **Get the code latest version**. Go to the directory of the code and do `git pull`
2. **Upgrade  your site  configuration**: Go to your site directory and use the upgrade command: `sitefab.py -c config/sitefab.yaml upgrade`. Replace `sitefab.yaml` with the name of your config. 
3. **Configure the new plugins and options*: Edit your plugins configuration file and make sure you have enabled the new plugins you want. The default plugins file being `config/plugins.yaml`