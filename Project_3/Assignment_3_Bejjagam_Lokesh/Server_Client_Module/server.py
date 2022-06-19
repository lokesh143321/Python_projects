"""server module"""
import socket
import server_functions

if __name__ == '__main__':
    HOST = 'local host'
    PORT = 8088
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    server.listen(5)

    server_Obj = server_functions.server_func()

    client, addr = server.accept()
    print("CONNECTION FROM:", str(addr))
    print("Server is Up and Running...")

    server_Obj.heading(client)

    while True:
        # option section
        OPTION_STATUS = server_Obj.options(client)
        if OPTION_STATUS == -1:
            print("Error in Option Section")
            break
        while OPTION_STATUS == 0:
            OPTION_STATUS = server_Obj.options(client)

        # command section
        if OPTION_STATUS == 1:
            # registration section
            COMMAND_STATUS = server_Obj.registration(client)
            while COMMAND_STATUS == 0:
                COMMAND_STATUS = server_Obj.registration(client)
            continue

        elif OPTION_STATUS == 2:
            # login section
            COMMAND_STATUS = server_Obj.login(client)
            while COMMAND_STATUS == 0:
                COMMAND_STATUS = server_Obj.login(client)

            # functions... after LOGIN...
            # command list section
            command_list_status = server_Obj.command_list(client)
            if command_list_status == 0:
                break

            # function command section
            FUNC_COMMAND = server_Obj.function_page(client)
            while FUNC_COMMAND != 0:
                FUNC_COMMAND = server_Obj.function_page(client)
            break

        else:
            # final option = 3 [QUIT]
            COMMAND_STATUS = server_Obj.quit(client)

        if COMMAND_STATUS == -1:
            print("Error in Command Section")
            break
        break

    client.close()
