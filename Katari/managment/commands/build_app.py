import os
import site
import sys
from shutil import copy2
from Katari.managment.commands import BaseCommand


class BuildApp(BaseCommand):

    def __init__(self, directory=None):
        self.bash_red = "\033[91m"
        self.bash_green = "\033[92m"
        self.end_bash_colour = "\033[0m"

        if not self._valid_project_name(directory): self.exit()
        self.directory = directory
        self.katari_path = "/Katari/template"


    def execute(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            self.copy_template(self._find_katari(), self.directory)
            print(self.bash_green + "Project Created" + self.end_bash_colour)
            sys.exit()
        print(self.bash_red + "Project {} already exists!".format(self.directory) + self.end_bash_colour)


    def _find_katari(self):
        for path in site.getsitepackages():
            if os.path.exists(path + self.katari_path):
                return path + self.katari_path  
        raise Exception(self.bash_red +"Unable to find Katari"+ self.end_bash_colour)

    def _valid_project_name(self, directory):
        if directory == "build-app":
            return False
        return True

    def copy_template(self, src_loc, dst_loc):
        for file in os.listdir(src_loc):
            if file[:2] != "__":
                try:
                    copy2(src_loc + "/" + file, dst_loc)
                except IOError:
                    print("Somthing bad happened....")

    def exit(self):
        print(self.bash_red + "Not a valid project name !" + self.end_bash_colour)
        sys.exit()











