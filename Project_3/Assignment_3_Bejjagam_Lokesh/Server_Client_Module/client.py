import socket
import client_functions

if __name__ == "__main__":
    port = 8088
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', port))

    client_Obj = client_functions.client_func()
    client_Obj.heading(client)

    while True:
        # option section
        option_status, option = client_Obj.options(client)
        if option_status == "quit":
            break
        while option_status == "failed":
            option_status, option = client_Obj.options(client)

        # command section
        if option == 1:
            # registration section
            command_status = client_Obj.registration(client)
            while command_status == "failed":
                command_status = client_Obj.registration(client)
            continue

        elif option == 2:
            # login section
            command_status = client_Obj.login(client)
            while command_status == "failed":
                command_status = client_Obj.login(client)

            # functions... after LOGIN...
            # command list section
            command_list_status = client_Obj.command_list(client)
            if command_list_status == "quit":
                break

            # function command section
            func_command = client_Obj.functionHandling(client)
            while func_command != "quit":
                func_command = client_Obj.functionHandling(client)
            break

        else:
            # final option = 3 [QUIT]
            command_status = "quit"

        if command_status == "quit":
            break

        break

    client.close()
