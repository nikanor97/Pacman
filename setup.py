from cx_Freeze import setup, Executable

from config import PATH_IMAGE


executables = [Executable('pacman_main.py',
                          targetName='Pacman.exe',
                          base='Win32GUI',
                          icon=f'{PATH_IMAGE}\\pacman.ico')]

includes = ['pygame', 'pygame_menu', 'os']

zip_include_packages = ['pygame', 'pygame_menu', 'os']

include_files = ['img/',
                 'config.py',
                 'field.py',
                 'field_config_points.py',
                 'field_config_relations.py',
                 'ghost.py',
                 'mob.py',
                 'pacman.py',

                 ]

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='pacman_main',
      version='0.1',
      description='Pacman game',
      executables=executables,
      options=options
      )
