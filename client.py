from struct import *
import socket 
import ctypes

serverIP = 'localhost'
serverPort = 12345

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

while True:
    operation = input("Enter operation (A, B, C, E): ")
    
    if operation == 'A':
        num_count = int(input("Enter number of integers (2 to 10): "))
        
        numbers = input(f"Enter {num_count} space-separated integers (-100 to 100): ").split()
        
        numbers = [int(num) for num in numbers]
        
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |      Length     |
        #  +----------------+-----------------+
        #  |Operat.|Num_cou |Padding |Padding |
        #  +----------------+--------+--------+
        #  |   N   |   N    |   N    |Padding |
        #  +----------------+-----------------+
        
        msg_type = 0
        msg_length = 2 * 4 +  len(numbers)
        msg_padSize = (4 - msg_length % 4) % 4

        message = ctypes.create_string_buffer(msg_length + msg_padSize)

        pack_into('!H', message, 0, msg_type)
        pack_into('!H', message, 2, msg_length)
        pack_into('!c', message, 4, operation.encode())
        pack_into('!B', message, 5, num_count)
        pack_into('xx', message, 6)
        offset = 8

        # Pack numbers into the buffer
        for number in numbers:
            pack_into('!b', message, offset, number)
            offset += 1

        # Add padding if necessary
        if msg_padSize > 0:
            pack_into(str(msg_padSize) + 'x', message, offset)

        # Send the message through the socket
        clientSocket.sendall(message)
        
    elif operation == 'B':
        num_count = int(input("Enter number of integers (2 to 20): "))
        
        numbers = input(f"Enter {num_count} space-separated integers (0 to 200): ").split()
        
        numbers = [int(num) for num in numbers]
        
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |      Length     |
        #  +----------------+-----------------+
        #  |Operat.|Num_cou |Padding |Padding |
        #  +----------------+--------+--------+
        #  |   N   |   N    |   N    |Padding |
        #  +----------------+-----------------+
        
        msg_type = 0
        msg_length = 2 * 4 +  len(numbers)
        msg_padSize = (4 - msg_length % 4) % 4

        message = ctypes.create_string_buffer(msg_length + msg_padSize)

        pack_into('!H', message, 0, msg_type)
        pack_into('!H', message, 2, msg_length)
        pack_into('!c', message, 4, operation.encode())
        pack_into('!B', message, 5, num_count)
        pack_into('xx', message, 6)
        offset = 8

        # Pack numbers into the buffer
        for number in numbers:
            pack_into('!B', message, offset, number)
            offset += 1

        # Add padding if necessary
        if msg_padSize > 0:
            pack_into(str(msg_padSize) + 'x', message, offset)

        # Send the message through the socket
        clientSocket.sendall(message)
        
    
    elif operation == 'C':
        num_count = int(input("Enter number of integers (2 to 10): "))
        
        numbers1 = input(f"Enter {num_count} space-separated integers for the first set (0 to 60000): ").split()
        numbers2 = input(f"Enter {num_count} space-separated integers for the second set (0 to 60000): ").split()
    
        numbers1 = [int(num) for num in numbers1]
        numbers2 = [int(num) for num in numbers2]
        
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |      Length     |
        #  +----------------+-----------------+
        #  |Operat.|Num_cou |len(num)|Padding |
        #  +----------------+--------+--------+
        #  |       N        |        N        |
        #  +----------------+-----------------+        
        #  |       N        |        N        |
        #  +----------------+-----------------+        
        #  |       N        |      Padding    |
        #  +----------------+-----------------+        

        msg_type = 0 
        msg_length = 2 * 4 +  2*(len(numbers1) + len(numbers2))
        msg_padSize = (4 - msg_length % 4) % 4

        message = ctypes.create_string_buffer(msg_length + msg_padSize)

        pack_into('!H', message, 0, msg_type)
        pack_into('!H', message, 2, msg_length)
        pack_into('!c', message, 4, operation.encode())
        pack_into('!B', message, 5, num_count)
        pack_into('!B', message, 6, len(numbers1))
        pack_into('x', message, 7)
        offset = 8

        # Pack numbers into the buffer
        for number in numbers1:
            pack_into('!H', message, offset, number)
            offset += 2
        for number in numbers2:
            pack_into('!H', message, offset, number)
            offset += 2

        # Add padding if necessary
        if msg_padSize > 0:
            pack_into(str(msg_padSize) + 'x', message, offset)

        # Send the message through the socket
        clientSocket.sendall(message)

    elif operation == 'E':

        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |      Length     |
        #  +----------------+-----------------+
        #  |Operat.|Padding |Padding |Padding |
        #  +----------------+--------+--------+

        msg_type = 0
        msg_length = 2*4
        msg_padSize = (4 - msg_length % 4) % 4

        message = ctypes.create_string_buffer(msg_length + msg_padSize)

        pack_into('!H', message, 0, msg_type)
        pack_into('!H', message, 2, msg_length)
        pack_into('!c', message, 4, operation.encode())
        pack_into('xxx', message, 5)

        # Send the message through the socket
        clientSocket.sendall(message)
        break
    
    else:
        
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |      Length     |
        #  +----------------+-----------------+
        #  |Operat.|Padding |Padding |Padding |
        #  +----------------+--------+--------+
        
        msg_type = 0
        msg_length = 2*4
        msg_padSize = (4 - msg_length % 4) % 4

        message = ctypes.create_string_buffer(msg_length + msg_padSize)

        pack_into('!H', message, 0, msg_type)
        pack_into('!H', message, 2, msg_length)
        pack_into('!c', message, 4, operation.encode())
        pack_into('xxx', message, 5)

        # Send the message through the socket
        clientSocket.sendall(message)
        
    #  0               16                31
    #  +----------------+-----------------+
    #  |      Type      |Response|Operat  |
    #  +----------------+-----------------+
    #  |               ...                |
    #  +----------------+--------+--------+
    
    response = clientSocket.recv(1024)

    msg_type, response_code, operation = unpack_from('!HBc', response, 0)
    operation=operation.decode()

    if response_code == 0:
        if operation == 'A':
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |Response|Operat  |
        #  +----------------+-----------------+
        #  |     Result     |Padding |Padding |
        #  +----------------+--------+--------+
            result, = unpack_from('!h', response, 4)
            print('The sum of the numbers is: ', result)
        elif operation == 'B':
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |Response|Operat  |
        #  +----------------+-----------------+
        #  |              Result              |
        #  +----------------+--------+--------+
            result, = unpack_from('!f', response, 4)
            print('The avg of the numbers is: ', result)
        elif operation == 'C':
        #  0               16                31
        #  +----------------+-----------------+
        #  |      Type      |Response|Operat  |
        #  +----------------+-----------------+
        #  |             Result1              |
        #  +----------------+--------+--------+
        #  |             Result2              |
        #  +----------------+--------+--------+
            result1, result2 = unpack_from('!II', response, 4)
            print('The sum from the two sets of numbers is: [', result1, ',', result2, ']')
    elif response_code == 1:
        print("Invalid operation")
    elif response_code == 2:
        print("Invalid input. Please enter a number between 2 and 10.")
    elif response_code == 3:
        print("Invalid input. Please enter a number between 2 and 20.")
    elif response_code == 4:
        print("Invalid input. Integers should be between -100 and 100.")
    elif response_code == 5:
        print("Invalid input. Integers should be between 0 and 200.")
    elif response_code == 6:
        print("Invalid input. Integers should be between 0 and 60000.")
    elif response_code == 7:
        print("Invalid input. Please enter the correct number of integers.")
        
        
