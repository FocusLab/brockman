from distutils.core import setup

setup(
    name='brockman',
    description='A Python client for the FocusLab API',
    url="https://github.com/FocusLab/brockman",
    version='0.1dev',
    packages=['brockman',],
    license='BSD',
    long_description=open('README.md').read(),
    author="Sean O'Connor",
    author_email="sean@focuslab.io",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
