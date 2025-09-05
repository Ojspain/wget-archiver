from setuptools import setup, find_packages

setup(
    name='wget-archiver',
    version='0.1.0',
    py_modules=['wget_archiver'],
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
    ],
    entry_points={
        'console_scripts': [
            'wget-archiver = wget_archiver:main',
        ],
    },
    author='Oliver Spain',
    author_email='oliverjspain@gmail.com',
    description='A general-purpose web scraper for archives.',
    long_description='A script that scrapes a given URL, either by following "next" links or by iterating through numbered pages, to collect all article URLs.',
    long_description_content_type='text/plain',
    url='https://github.com/Ojspain/wget-archiver',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
