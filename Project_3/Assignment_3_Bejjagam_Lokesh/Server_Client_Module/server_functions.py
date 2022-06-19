'''Server functions'''
import json
import re
import os

main_path = os.getcwd()
os.chdir("root")
current_user = list()

class server_func:
    """
    class server_func

    Attributes:
        login_reg : regex
        registration_reg : regex

    Methods:
        Used to do proper communication with the client

    """

    login_reg = "login [a-zA-Z0-9]+ [a-zA-Z0-9]+"
    registration_reg = "register [a-zA-Z0-9]+ [a-zA-Z0-9]+"

    def data_read(self):
        """
        :return: dict_data
        :rtype: dictionary
        """
        try:
            change_in_path = os.getcwd()
            os.chdir(main_path)
            with open("client.json", "r") as file:
                dict_data = json.load(file)
            os.chdir(change_in_path)
        except:
            dict_data = {}
        return dict_data

    def data_write(self, msg):
        """
        :param msg: Data need to enter into the text file
        :type msg: list of string
        :return: none
        :rtype: none
        """
        dict_data = self.data_read()
        dict_data[msg[0]] = msg[1]

        change_in_path = os.getcwd()
        os.chdir(main_path)
        with open("client.json", "w") as file:
            json.dump(dict_data, file)

        os.chdir(change_in_path)

    def send(self, client, msg):
        """
        :param client: socket object
        :type client: socket
        :param msg: message -> send to the client
        :type msg: string
        :return:none
        :rtype: none
        """
        try:
            client.send(msg.encode())
        except:
            print("Message sending Error!")
            client.close()

    def receive(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: message -> received from client
        :rtype: string
        """
        try:
            msg = (client.recv(1024)).decode()
        except:
            print("Message Receiving Error!")
            msg = "Error"
        return msg

    def heading(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: none
        :rtype: none
        """
        msg = "<<<<< Server-Client File Management System >>>>>"
        self.send(client, msg)

    def options(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: options
        :rtype: integer
        """
        self.send(client, "Options:[Register->Press 1] *** [Login ->Press 2]***[Quit->Press 3]")
        try:
            option = int(self.receive(client))
            if option == 1 or option == 2 or option == 3:
                print("option received: ", option)
                self.send(client, "success")
                return int(option)
            else:
                print("Invalid Option")
                self.send(client, "failed")
                return 0
        except:
            print("Exception Error Invalid Option")
            self.send(client, "quit")
            return -1

    def registration(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: status
        :rtype: integer
        """
        self.send(client, "Enter Command: register <username> <password>")  # 3
        cmd = self.receive(client)

        matched = re.match(self.registration_reg, str(cmd))
        status = bool(matched)
        try:
            if status:
                cmd_list = cmd.split(" ")
                name = str(cmd_list[1])
                pwd = cmd_list[2]
                os.chdir(main_path + "\\root")
                os.mkdir(name)  # make directory for the user

                print("Registered " + name + " " + pwd + " successfully!")
                self.send(client, "success")  # 4
                self.data_write((name, pwd))
                return 1

            else:
                print("Registration is not successful..!")
                self.send(client, "failed")
                return 0
        except:
            print("Exception Error Invalid Registration")
            self.send(client, "quit")
            return -1

    def login(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: status
        :rtype: integer
        """
        self.send(client, "Enter Command: login <username> <password>")
        cmd = self.receive(client)

        matched = re.match(self.login_reg, str(cmd))
        status = bool(matched)

        try:
            if status:
                print(os.getcwd())
                cmd_list = cmd.split(" ")
                name = str(cmd_list[1])
                pwd = cmd_list[2]
                dict_data = self.data_read()

                if name in dict_data.keys():
                    if pwd == dict_data[name]:
                        os.chdir(main_path + "\\root")
                        os.chdir(name)
                        print("Login " + name + " " + pwd + " successfully!")
                        self.send(client, "success")
                        print(os.getcwd())
                        current_user.append(name)
                        return 1
                    else:
                        print("Login Password is not matching..!")
                        self.send(client, "failed")
                        return 0
                else:
                    print("No User Found..!")
                    self.send(client, "failed")
                    return 0
            else:
                self.send(client, "failed")
                return 0
        except:
            print("Exception Error Invalid Login")
            self.send(client, "quit")
            return -1

    def quit(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: none
        :rtype: none
        """
        client.close()

    def function_page(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: return_msg
        :rtype: integer
        """
        regEx_dict = dict({"login": "login [a-zA-Z0-9]+ [a-zA-Z0-9]+",
                           "register": "register [a-zA-Z0-9]+ [a-zA-Z0-9]+",
                           "change_folder": "change_folder [a-zA-Z0-9]+",
                           "list": "list",
                           "read_file": "read_file [a-zA-Z0-9]+",
                           "write_file": "write_file [a-zA-Z0-9.]+ [a-zA-Z0-9]+",
                           "create_folder": "create_folder [a-zA-Z0-9]+",
                           "commands": "commands",
                           "quit": "quit"})

        rcv_data = self.receive(client)  # receive
        rcv_dataSplit = rcv_data.split(" ")
        return_msg = 0
        if rcv_dataSplit[0] in regEx_dict.keys():
            matched = re.match(regEx_dict[rcv_dataSplit[0]], str(rcv_data))
            status = bool(matched)
            if status:
                return_msg = int(self.run_function(client, rcv_dataSplit))  # function performance
                if return_msg == 1:
                    if rcv_dataSplit[0] == "quit":
                        return_msg = 0
                        self.send(client, "quit")
                    else:
                        self.send(client, "success")
                else:
                    self.send(client, "failed")
            else:
                self.send(client, "failed")  # ackSend
        return return_msg

    def changefolder(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        try:
            if "root" == (os.getcwd()[-4:]):
                if func_cmd[1] != current_user[0] or func_cmd[1] == "..":
                    print("Path Error")
                    raise ValueError
                else:
                    os.chdir(func_cmd[1])
                    self.send(client, "Directory Changed Successful")
                    print("Directory Changed Successful")
                    return 1
            else:
                os.chdir(func_cmd[1])
                self.send(client, "Directory Changed Successful")
                print("Directory Changed Successful")
                return 1
        except:
            self.send(client, "Directory Changed unsuccessful")
            print("Directory Changed unsuccessful")
            return -1

    def list_func(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        try:
            directory_list = os.listdir(os.getcwd())
            if len(directory_list) > 0:
                self.send(client, str(directory_list))
                print("Directory List: ", directory_list)
            else:
                print("Directory Empty")
                self.send(client, "Directory Empty")
            return 1
        except:
            self.send(client, "Directory Not Found")
            print("Directory Not Found")
            return 0

    def read_file(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        try:
            with open(func_cmd[1], "r") as file:
                content = str(file.read())
                print("file content: ", content)
                self.send(client, content)
            return 1
        except:
            print("File Reading Error")
            self.send(client, "File Reading Error")
            return 0

    def write_file(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        try:
            with open(func_cmd[1], "a+") as file:
                data = "".join(str(character) + " " for character in func_cmd[2:])
                file.write("\n")
                file.write(data)
                self.send(client, "File Updated Successfully")
            return 1
        except:
            print("File Writing Error")
            self.send(client, "File Writing Error")
            return 0

    def create_folder(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        try:
            os.mkdir(func_cmd[1])
            print("Directory Created Successfully")
            self.send(client, "Directory Created Successfully")
            return 1
        except:
            print("Directory Created Unsuccessful")
            self.send(client, "Directory Created Unsuccessful")
            return 0

    def command_list(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: status
        :rtype: integer
        """
        try:
            commands = """***COMMANDS***\nCommand: change_folder <folder_Name>
            \nDescription: Used to move to the corresponding folder_Name
            \nCommand: list\nDescription: Used to print all the files and folders in the current directory
            \nCommand: read_file <file_Name>
            \nDescription: Used to read the contents of the file\nCommand: write_file <file_Name> <input_data>
            \nDescription: Used to write the <input_data> into the <file_Name>\nCommand: create_folder <folder_Name>
            \nDescription: Used to create a folder under the current directory
            \nCommand: commands\nDescription: Used to display the valid commands\nCommand: register <username> <password>
            \nDescription: Used to register a user
            \nCommand: login <username> <password>\nDescription: Used to login with registered valid user\nCommand: quit
            \nDescription: Used to disconnect from the server"""
            print("Command list sent successfully...")
            self.send(client, commands)
            return 1
        except:
            print("Command list sent unsuccessful...")
            self.send(client, "quit")
            return 0

    def run_function(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: list of command words
        :type func_cmd: list of strings
        :return: return_msg
        :rtype: integer
        """
        main_key = func_cmd[0]
        print(main_key)
        try:
            if "change_folder" == main_key:
                return_msg = self.changefolder(client, func_cmd)
            elif "list" == main_key:
                return_msg = self.list_func(client, func_cmd)
            elif "read_file" == main_key:
                return_msg = self.read_file(client, func_cmd)
            elif "write_file" == main_key:
                return_msg = self.write_file(client, func_cmd)
            elif "create_folder" == main_key:
                return_msg = self.create_folder(client, func_cmd)
            elif "commands" == main_key:
                return_msg = self.command_list(client)
            elif "quit" == main_key:
                return_msg = self.quit_func(client)
            elif "login" == main_key:
                return_msg = self.new_login(client, func_cmd)
            elif "register" == main_key:
                return_msg = self.new_registration(client, func_cmd)
            else:
                print("calling registration function")
                return_msg = self.new_registration(client, func_cmd)
        except:
            return_msg = 0
        return return_msg

    def quit_func(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: status
        :rtype: integer
        """
        try:
            self.send(client, "Session Ended Successful")
            print("Session Ended Successful")
            return 1
        except:
            self.send(client, "Session Ended unsuccessful")
            print("Session Ended unsuccessful")
            return 0

    def new_login(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: execution commands
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        cmd = "".join(str(character) + " " for character in func_cmd)
        cmd = cmd.strip()
        matched = re.match(self.login_reg, str(cmd))
        status = bool(matched)

        try:
            if status:
                print(os.getcwd())
                cmd_list = func_cmd.copy()
                name = str(cmd_list[1])
                pwd = cmd_list[2]
                dict_data = self.data_read()

                if name in dict_data.keys():
                    if pwd == dict_data[name]:
                        os.chdir(main_path + "\\root")
                        os.chdir(name)
                        print("Login " + name + " " + pwd + " successfully!")
                        self.send(client, "success")
                        print(os.getcwd())
                        current_user.append(name)
                        return 1
                    else:
                        print("Login Password is not matching..!")
                        self.send(client, "failed")
                        return 0
                else:
                    print("No User Found..!")
                    self.send(client, "failed")
                    return 0
            else:
                self.send(client, "failed")
                return 0
        except:
            print("Exception Error Invalid Login")
            self.send(client, "quit")
            return -1

    def new_registration(self, client, func_cmd):
        """
        :param client: socket object
        :type client: socket
        :param func_cmd: execution commands
        :type func_cmd: list of strings
        :return: status
        :rtype: integer
        """
        print(func_cmd)
        cmd = "".join(str(character) + " " for character in func_cmd)
        cmd = cmd.strip()
        print(cmd)
        matched = re.match(self.registration_reg, cmd)
        status = bool(matched)
        print(status)
        try:
            if status:
                cmd_list = func_cmd.copy()
                name = str(cmd_list[1])
                pwd = cmd_list[2]
                os.chdir(main_path + "\\root")
                os.mkdir(name)  # make directory for the user
                print(os.getcwd())

                print("Registered " + name + " " + pwd + " successfully!")
                self.send(client, "success")  # 4
                self.data_write((name, pwd))
                return 1
            else:
                print("Registration is not successful..!")
                self.send(client, "failed")
                return 0
        except:
            print("Exception Error Invalid Registration")
            self.send(client, "quit")
            return -1

    ###############Testing###################
    def test_registration(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        matched = re.match(self.registration_reg, str(cmd))
        status = bool(matched)
        try:
            if status:
                cmd_list = cmd.split(" ")
                name = str(cmd_list[1])
                pwd = cmd_list[2]

                os.chdir(main_path + "\\root")
                os.mkdir(name)

                print("Registered " + name + " " + pwd + " successfully!")

                self.data_write((name, pwd))
                return "success"

            else:
                print("Registration is not successful..!")
                return "failed"
        except:
            print("Exception Error Invalid Registration")
            return "quit"

    def test_login(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        matched = re.match(self.login_reg, str(cmd))
        status = bool(matched)
        try:
            if status:
                cmd_list = cmd.split(" ")
                name = str(cmd_list[1])
                pwd = cmd_list[2]
                dict_data = self.data_read()
                if name in dict_data.keys():
                    if pwd == dict_data[name]:
                        os.chdir(main_path + "\\root")
                        os.chdir(name)
                        print("Login " + name + " " + pwd + " successfully!")
                        return "success"
                    else:
                        print("Login Password is not matching..!")
                        return "failed"
                else:
                    print("No User Found..!")
                    return "failed"
            else:
                return "failed"
        except:
            print("Exception Error Invalid Login")
            return "quit"

    def test_commands_list(self):
        """
        :return: status
        :rtype: string
        """
        try:
            commands = """***COMMANDS***\nCommand: change_folder <folder_Name>
            \nDescription: Used to move to the corresponding folder_Name
            \nCommand: list\nDescription: Used to print all the files and folders in the current directory
            \nCommand: read_file <file_Name>
            \nDescription: Used to read the contents of the file\nCommand: write_file <file_Name> <input_data>
            \nDescription: Used to write the <input_data> into the <file_Name>\nCommand: create_folder <folder_Name>
            \nDescription: Used to create a folder under the current directory\nCommand: commands
            \nDescription: Used to display the valid commands\nCommand: register <username> <password>
            \nDescription: Used to register a user\nCommand: login <username> <password>
            \nDescription: Used to login with registered valid user\nCommand: quit
            \nDescription: Used to disconnect from the server"""
            print("Command list sent successfully...")
            return commands
        except:
            print("Command list sent unsuccessful...")
            return "failed"

    def test_create_folder(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        func_cmd = cmd.split(' ')
        try:
            os.mkdir(func_cmd[1])
            print("Directory Created Successfully")
            return "success"
        except:
            print("Directory Created Unsuccessful")
            return "failed"

    def test_change_folder(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        func_cmd = cmd.split(' ')
        try:
            os.chdir(func_cmd[1])
            print("Directory Changed Successful")
            return "success"
        except:
            print("Directory Changed unsuccessful")
            return "failed"

    def test_read_file(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        func_cmd = cmd.split(' ')
        try:
            with open(func_cmd[1], "r") as file:
                content = str(file.read())
                print("file content: ", content)
            return "success"
        except:
            print("File Reading Error")
            return "failed"

    def test_write_file(self, cmd):
        """
        :param cmd: execution command
        :type cmd: string
        :return: status
        :rtype: string
        """
        func_cmd = cmd.split(' ')
        try:
            with open(func_cmd[1], "w") as file:
                data = "".join(str(character) + " " for character in func_cmd[2:])
                file.write("\n")
                file.write(data)
            return "success"
        except:
            print("File Writing Error")
            return "failed"
