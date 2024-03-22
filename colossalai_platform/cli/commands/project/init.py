import os
import shutil

import click


@click.command(help='Initialize Your ColossalAI Template')
@click.argument('name', required=1, type=str)
def init(name):
    # get current directory
    current_dir = os.getcwd()

    # create the project directory
    user_project_dir = os.path.join(current_dir, name)

    if os.path.exists(user_project_dir):
        click.echo(f"Error: The project {name} already exists in {current_dir}")
        exit()
    else:
        os.mkdir(user_project_dir)

    # get the current file path
    # the project files are located in current_file_path/project_template
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    project_file_dir = os.path.join(current_file_path, 'project_template')

    # copy the files in project_file_dir to template_dir
    for file_name in os.listdir(project_file_dir):
        # skip this file
        if file_name in ['__init__.py', '__pycache__']:
            continue

        src_path = os.path.join(project_file_dir, file_name)
        dst_path = os.path.join(user_project_dir, file_name)

        if file_name == "README.md":
            # replace project name in README.md
            with open(src_path, 'r') as src_f:
                lines = src_f.readlines()

            # replace <Project-Name> with the actual name
            lines = [line.replace('<Project-Name>', name) for line in lines]

            # write to the new file
            with open(dst_path, 'w') as dst_f:
                dst_f.writelines(lines)
        else:
            shutil.copy(src_path, dst_path)

    click.echo(f"""Project skeleton `{name}` has been initialized in `{user_project_dir}`
    
- Edit `train.sh`, `train.py` and `HyperParameters.json` to create your own training project.
- To upload it to the platform, run `cap project create` and `cap project upload-dir`.
""")
