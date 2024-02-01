from setuptools import setup, find_packages

setup(
    name='DocReaderAI',
    version='1.0.0',
    packages=find_packages(),
    description='A Pdf Reader AI',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='GPTVerse',
    author_email='support@gptverse.art',
    include_package_data=True,
    install_requires=[
         'dacite==1.8.1',
        'icecream==2.1.3',
        'langchain==0.0.353',
        'pydantic==1.10.13',
        'tenacity==8.2.2',
        'tiktoken==0.5.1',
        'openai==0.28.1'
    ],
)
