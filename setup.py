from setuptools import setup, find_packages

setup(
    name='archive-scraper',
    version='1.0.0',
    py_modules=['link_grabber'],
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
    ],
    entry_points={
        'console_scripts': [
            'archive-scraper = link_grabber:main',
        ],
    },
    author='Oliver Spain',
    author_email='oliverjspain@gmail.com',
    description='A general-purpose web scraper for archives.',
    long_description='A script that scrapes a given URL, either by following "next" links or by iterating through numbered pages, to collect all article URLs. It can also download the pages using wget.',
    long_description_content_type='text/plain',
    url='https://github.com/PLACEHOLDER',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
