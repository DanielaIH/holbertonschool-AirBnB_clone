#!/usr/bin/python3
"""HBNBCommand contains the entry point of the command interpreter:"""

from hashlib import new
import models
import cmd
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel, "User": User, "Amenity": Amenity,
               "City": City, "Place": Place, "Review": Review, "State": State}

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def do_create(self, arg):
        """create - create method"""
        arg = arg.split()
        if len(arg) == 0:
            print("** class name missing **")
            return False
        elif arg[0] in HBNBCommand.classes:
            posti = self.classes[arg[0]]()
        else:
            print("** class doesn't exist **")
            return
        print(posti.id)
        posti.save()

    def do_show(self, arg):
        """Function show """
        arg = arg.split()
        all_objs = models.storage.all()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif arg[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        elif f'{arg[0]}.{arg[1]}' in all_objs.keys():
            print(all_objs[f"{arg[0]}.{arg[1]}"])
            return
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based id"""
        arg = arg.split()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        else:
            stor = storage.all()
            space = arg[0] + '.' + arg[1]
            no_instance = False
            for key in stor.copy().keys():
                if space in key:
                    del stor[str(space)]
                    storage.save()
                    no_instance = True

            if not no_instance:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        str_ins = arg.split()
        all_objs = models.storage.all()
        if not arg or str_ins[0] in HBNBCommand.classes:
            str_rep = []
            for obj in all_objs.values():
                str_rep.append(obj.__str__())
            print(f"{str_rep}")
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        arg = arg.split()
        arg = arg[0:4]
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif len(arg) == 2:
            print("** attribute name missing **")
        elif len(arg) == 3:
            print("** value missing **")
        else:
            objs = models.storage.all()
            camps = "{}.{}".format(arg[0], arg[1])
            if camps in objs.keys():
                for value in objs.values():
                    try:
                        atribute = type(getattr(value, arg[2]))
                        arg[3] = atribute(arg[3])
                    except AttributeError:
                        pass
                    setattr(value, arg[2], arg[3].strip('"'))
                    models.storage.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
