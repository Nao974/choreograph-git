# -*-coding:Utf-8 -*

"""Docstring d'une ligne décrivant brièvement ce que fait le programme.

Usage:
======
    python nom_de_ce_super_script.py argument1 argument2

    argument1: un entier signifiant un truc
    argument2: une chaîne de caractères décrivant un bidule
"""

__authors__ = "François BOLDODUCK"
__contact__ = "nao-tumu@hotmail.fr"
__version__ = "0.9.0"
__date__ = "2020/11"

from interface.interface import *
import common.constants as g
import platform

g.system = platform.uname()
version = __version__ +' '+ __date__
lang = lang_FR
bye = 'N'

while bye != 'Q':
    try:
        interface = Interface(version, lang)
        interface.windows.mainloop()
        lang = interface.get_lang()
        bye = interface.get_bye()
    except :
        pass
