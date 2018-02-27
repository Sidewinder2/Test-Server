import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = '192.168.95.145'
host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
#host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

shutdown = False

ping_period = 5
ping_timer = 0;

while not shutdown:
    c, addr = s.accept()     # Establish connection with client.
    print('GOT CONNECTION FROM', addr)
    #c.send(b'Thank you for connecting')
    client_input = ""
    server_output = ""
    close_connection = False
    while client_input != "exit" or close_connection:
        try:
            c.settimeout(1)
            # get info from client, if any was sent
            client_input = c.recv(1024).decode()
            if len(client_input) > 0:
                print(client_input)
                if client_input == "hello":     # basic client function testing
                    server_output = "world"
                    c.send(server_output.encode())
                if client_input == "shutdown":  # function to shut down server
                    server_output = "Exiting"
                    c.send(server_output.encode())
                    shutdown = True
                    break
            # check if connection was lost
            if len(client_input) == 0:
                print("CONNECTION LOST")
                break

        except Exception as e:
            if str(e) != "timed out":
                print(e)

        # spam client
        try:
            # send spam to the client every few seconds
            ping_timer += 1
            if ping_timer == ping_period:
                ping_timer = 0
                server_output = "ping"
                c.send(server_output.encode())
        except Exception as e:
            if str(e) != "timed out":
                print(e)

    print("CLOSING CONNECTION");
    c.close()                # Close the connection

    if (shutdown):
        print("SHUTTING DOWN")
