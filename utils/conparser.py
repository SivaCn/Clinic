
import os
import ConfigParser

base_dir = os.path.abspath(".")
products_dir = os.path.join(base_dir, r'products')


class Config(object):
    """
    """
    def __init__(self, _dir, configFile=r'config.ini'):
        """
        """
        config_file_path = os.path.join(_dir, configFile)

        if not os.path.exists(config_file_path):
            print "Specified config file does not Exist"
            return None

        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file_path)


    def get(self, section, option):
        """
        """
        return self.config.get(section, option)


config = Config(base_dir, r'config.ini')
proConfig = Config(products_dir, r'config.ini')

import pdb; pdb.set_trace() # BREAKPOINT
print ""
