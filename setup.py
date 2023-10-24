from setuptools import setup, find_packages

setup(
    name='cfa_analysis',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.py']
    },
    # entry_points={
    #     'console_scripts': [
    #         'cfa_analysis = cfa_analysis.main:main'
    #     ]
    # },
    install_requires=[
        'pandas',
        'requests',
        'bokeh',
        'statistics',
        'numpy',
        'jupyter_ai',
    ],
)