# Modify template description and variables

You have the option to add your own description template under the folder `templates/`. We use Jinja2 (https://palletsprojects.com/p/jinja/) for templating.

If you want to use your own template instead of our default template do the following:

1. Create a new template under `templates` with the file extension `.j2`
2. Add the argument `--template_name` with your template file
