"""client module"""
class client_func:

    def send(self, client, msg):
        """
        :param client: socket object
        :type client: socket
        :param msg: message -> send to the server
        :type msg: string
        :return: none
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
        :return: msg
        :rtype: string
        """
        try:
            msg = (client.recv(1024)).decode()
        except:
            print("Message Receiving Error!")
            msg = "Error"

        return msg
    def heading(self, client):
        print(self.receive(client))

    def options(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: ackmsg and option
        :rtype: string and integer
        """
        server_msg = self.receive(client)  # 1
        print(server_msg)

        option = input(":>>>")
        self.send(client, option)

        ack_msg = self.receive(client)  # 2
        print("feedback: ", ack_msg)
        return ack_msg, int(option)

    def registration(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: ackmsg
        :rtype: string
        """
        server_msg = self.receive(client)  # 3
        print(server_msg)

        cmd = input(":>>>")
        self.send(client, cmd)

        ack_msg = self.receive(client)  # 4
        print("feedback: ", ack_msg)
        return ack_msg

    def login(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: ackmsg
        :rtype: string
        """
        server_msg = self.receive(client)  # 3
        print(server_msg)

        cmd = input(":>>>")
        self.send(client, cmd)

        ack_msg = self.receive(client)  # 4
        print("feedback: ", ack_msg)
        return ack_msg

    def functionHandling(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: ackmsg
        :rtype: string
        """
        func_cmd = input(":>>>")
        self.send(client, func_cmd)

        self.run_func(client)

        ack_msg = self.receive(client)  # 4
        print(ack_msg)
        if "quit" in func_cmd:
            ack_msg = "quit"
        return ack_msg

    def command_list(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: status
        :rtype: string
        """
        server_msg = self.receive(client)
        print(server_msg)

        if server_msg == "quit":
            return "quit"
        else:
            return "success"

    def run_func(self, client):
        """
        :param client: socket object
        :type client: socket
        :return: none
        :rtype: none
        """
        server_msg = self.receive(client)  # 3
        print(server_msg)
