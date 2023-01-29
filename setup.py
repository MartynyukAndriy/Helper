setup(
    name='Helper',
    version='0.0.1',
    description='Personal Assistant "Helper" with a command line interface',
    url='https://github.com/MartynyukAndriy/Helper',
    author='Martynyuk Andriy, Dmytro Poznanskyi, Mykola Tyshko, Dmytro Lyfenko, Roman Ovcharenko',
    author_email='andriy.martynyuk.if@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['helper = helper.main:main']}
)
