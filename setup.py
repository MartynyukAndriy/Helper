from setuptools import setup, find_namespace_packages

setup(
    name='Helper_assistant_bot',
    version='0.0.1',
    description='Personal Assistant "Helper" with a command line interface',
    url='https://github.com/MartynyukAndriy/Helper',
    author='Martynyuk Andriy, Dmytro Poznanskyi, Mykola Tyshko, Dmytro Lyfenko, Roman Ovcharenko',
    author_email='andriy.martynyuk.if@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    data_files=[("Helper", ["Helper/address_book.py", "Helper/bot.py",
                 "Helper/classes.py", "Helper/notes.py", "Helper/sort.py", "Helper/translate.py"])],
    entry_points={'console_scripts': ['helper = Helper.helper:main']}
)
