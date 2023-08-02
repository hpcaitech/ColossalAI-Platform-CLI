import os

from setuptools import find_packages, setup


def fetch_requirements(path):
    with open(path, 'r') as fd:
        return [r.strip() for r in fd.readlines()]


def fetch_readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def get_version():
    with open('version.txt') as f:
        return f.read().strip()


def get_project_files():
    # get current file dir directory
    # the templates files are located in current_file_path/templates
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    project_file_dir = os.path.join(current_file_path, 'colossalai_platform/cli/commands/projects')
    
    # get all the files in project_file_dir
    project_files = []
    
    for file_name in os.listdir(project_file_dir):
        project_files.append(os.path.join(project_file_dir, file_name))
    return project_files


setup(
    name='colossalai-platform',
    version=get_version(),
    packages=find_packages(exclude=(
        'build',
        'docker',
        'tests',
        'docs',
        'examples',
        '*.egg-info',
    )),
    description='ColossalAI Platform CLI for ease',
    long_description=fetch_readme(),
    long_description_content_type='text/markdown',
    license='Apache Software License 2.0',
    url='https://github.com/hpcaitech/ColossalAI-Platform-CLI',
    project_urls={
        'Github': 'https://github.com/hpcaitech/ColossalAI-Platform-CLI',
    },
    package_data={'': get_project_files()},
    include_package_data=True,
    install_requires=fetch_requirements('requirements.txt'),
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        cap=colossalai_platform.cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Build Tools',
        "Topic :: System :: Distributed Computing"
    ],
)
