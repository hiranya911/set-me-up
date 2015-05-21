#!/usr/bin/python

import sys
import os
import optparse

"""
Defines the basic attributes of a project and the operations to persist project
metadata to the disk.
"""
class Project:
    def __init__(self, project_home = None):
        self.name = None
        self.description = None
        self.langs = None
        self.techs = None
        self.status = None
        if project_home != None:
            meta = open(project_home + os.sep + ".meta", "r")
            lines = meta.readlines()
            for line in lines:
                if len(line.strip()) == 0:
                    continue
                (key,value) = line.split("=")        
                if key == "Name":
                    self.name = value.strip()
                elif key == "Description":
                    self.description = value.strip()
                elif key == "Languages":
                    self.langs = value.strip()
                elif key == "Technologies":
                    self.techs = value.strip()
                elif key == "Status":
                    self.status = value.strip()
            meta.close()
            
    def __str__(self):
        string = "Name: " + self.name + "\n"
        string += "Languages: " + self.langs + "\n"
        string += "Technologies: " + self.techs + "\n"
        string += "Status: " + self.status + "\n"
        string += "Description: " + self.description
        return string

    def __repr__(self):
        string = "Name=" + self.name + "\n"
        string += "Languages=" + self.langs + "\n"
        string += "Technologies=" + self.techs + "\n"
        string += "Status=" + self.status + "\n"
        string += "Description=" + self.description + "\n"
        return string

    def create(self, project_home):
        os.mkdir(project_home)
        os.mkdir(project_home + os.sep + "impl")
        os.mkdir(project_home + os.sep + "research")
        os.mkdir(project_home + os.sep + "sandbox")
        self.save_data(project_home)

    def save_data(self, project_home):
        meta = open(project_home + os.sep + ".meta", "w")
        meta.write(`self`)
        meta.close()

def die(msg):
    print 'Error:', msg
    quit()

def create_project(fileName):
    if len(fileName) == 0:
        die("A file name must be specified to create a project")
        
    for char in fileName:
        if char.isupper() or (not char.isalnum() and char != '-'):
            die("Invalid character '" + char + "' in file name. Only lower case letters, digits and hyphens are allowed.")

    if os.path.exists(fileName):
        die("A file named '" + fileName + "' exists already")

    info = get_project_info()
    project = Project()
    project.name = info[0]
    project.langs = info[1]
    project.techs = info[2]
    project.description = info[3]
    project.status = "Active"
    project.create(fileName)
    print "Project created successfully"

def get_project_info(update=False):
    name = raw_input("Project name: ")
    if update:
        while name.strip() == ":d":
            name = raw_input("Project name must not be empty. Please try again: ")
    else:
        while len(name.strip()) == 0:
            name = raw_input("Project name must not be empty. Please try again: ")
    langs = raw_input("Languages used (comma separated list): ")
    techs = raw_input("Other technologies used (comma separated list): ")
    desc = raw_input("Description: ")
    return (name.strip(), langs.strip(), techs.strip(), desc.strip())

def describe_project():
    project = load_project()
    print project,

def update_project():
    project = load_project()
    print "Hit enter to leave the existing value unchanged. Enter ':d' to delete an existing value."
    info = get_project_info(True)
    if len(info[0]) != 0:
        project.name = get_updated_value(info[0])
        if len(info[1]) != 0:
            project.langs = get_updated_value(info[1])
        if len(info[2]) != 0:
            project.techs = get_updated_value(info[2])
        if len(info[3]) != 0:
            project.description = get_updated_value(info[3])
        project.save_data(".")

def get_updated_value(value):
    return value if value != ":d" else ""

def set_project_status(status):
    project = load_project()
    if project.status != status:
        project.status = status
        project.save_data(".")
        print "Project status set to '" + status + "'"
    else:
        print "Project is already in the '" + status + "' state"

def list_projects(recursive):
    project = load_project('.', False)
    if project != None:
        print project.name + "\t\t" + os.path.abspath(".")

    if recursive:
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                list_project_entry(dirname, subdirname)
    else:        
        for name in os.listdir('.'):
            list_project_entry('.', name)

def list_project_entry(dirname, subdirname):
    path = os.path.join(dirname, subdirname)
    project = load_project(path, False)
    if project != None:
        print project.name + " - " + os.path.abspath(path)
                             
def load_project(project_home = ".", die_on_error = True):
    try:
        project = Project(project_home)
        return project
    except IOError:
        if die_on_error:
            die("No project found in the current directory")
        else:
            return None

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-c", "--create", action="store", type="string", dest="new_project_name")
    parser.add_option("-u", "--update", action="store_true", dest="update")
    parser.add_option("-d", "--deactivate", action="store_true", dest="deactivate")
    parser.add_option("-a", "--activate", action="store_true", dest="activate")
    parser.add_option("-l", "--list", action="store_true", dest="list")
    parser.add_option("-r", "--recursive", action="store_true", dest="recursive")
    (options,args) = parser.parse_args(sys.argv[1:])
    if options.new_project_name != None:
        create_project(options.new_project_name)
    elif options.update:
        update_project()
    elif options.activate:
        set_project_status("Active")
    elif options.deactivate:
        set_project_status("Inactive")
    elif options.list:
        list_projects(options.recursive)
    else:
        describe_project()
