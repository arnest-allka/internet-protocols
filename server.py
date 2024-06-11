import socket
from struct import *
from _thread import *

serverIP = 'localhost'
serverPort= 12345

close = False

def addittion(numbers):
    return sum(numbers)
    

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def add_number_sets(set1, set2):
    return [x + y for x, y in zip(set1, set2)]
    
def thread_client(conn,addr):
    
    print("Connected by:", addr)
    print("Server Socket port: ", conn.getsockname())
    print("Client Socket port: ", conn.getpeername())
    
    while(True):
        
        data = conn.recv(1024)
        if not data:
            break
        
        msg_type, msg_length = unpack_from('!HH', data, 0)
        operation, num_count = unpack_from('!cB', data, 4)
        operation = operation.decode()
        response_code=0
        
        if operation=='A': 
            if num_count < 2 or num_count > 10:
                print("Invalid input. Please enter a value between 2 and 10.")
                response_code = 2
            else:
                numbers = []
                offset = 8
                while(True):
                    number, = unpack_from('!b', data, offset)
                    if number:
                        if number < -100 or number > 100:
                            print("Invalid input. Integers should be between -100 and 100.")
                            response_code = 4
                            break
                        else:
                            numbers.append(number)
                            offset += 1
                    else:
                        break
                
                if response_code == 0:        
                    if len(numbers) != num_count:
                        print("Invalid input. Please enter the correct number of integers.")
                        response_code = 7                    
                    else:
                        print(f"Message Type: {msg_type}")
                        print(f"Message Length: {msg_length}")
                        print(f"Operation: {operation}")
                        print(f"Number Count: {num_count}")
                        print(f"Numbers: {numbers}")
                        
                        result = addittion(numbers)

        elif operation == 'B':                
            if num_count < 2 or num_count > 20:
                print("Invalid input. Please enter a value between 2 and 20.")
                response_code = 3
            else:
                numbers = []
                offset = 8
                while(True):
                    number, = unpack_from('!B', data, offset)

                    if number:
                        if number < 0 or number > 200:
                            print("Invalid input. Integers should be between 0 and 200.")
                            response_code = 5
                            break
                        else:
                            numbers.append(number)
                            offset += 1
                    else:
                        break
                    
                    print(numbers)
                    
                if response_code == 0:
                    if len(numbers) != num_count:
                        print("Invalid input. Please enter the correct number of integers.")
                        response_code = 7                    
                    else:
                        print(f"Message Type: {msg_type}")
                        print(f"Message Length: {msg_length}")
                        print(f"Operation: {operation}")
                        print(f"Number Count: {num_count}")
                        print(f"Numbers: {numbers}")
                        
                        result = calculate_average(numbers)

        elif operation == 'C':
            if num_count < 2 or num_count > 10:
                print("Invalid input. Please enter a value between 2 and 10.")
                response_code = 2
            else:
                midPoint, = unpack_from('!B', data, 6)
                print(midPoint)
                numbers = []
                offset = 8
                
                while True:
                    if offset + 2 > msg_length:
                        break
                    
                    number, = unpack_from('!H', data, offset)
                    print(number)
                    if number:
                        if number < 0 or number > 200:
                            print("Invalid input. Integers should be between 0 and 200.")
                            response_code = 5
                            break
                        else:
                            numbers.append(number)
                            offset += 2
                    else:
                        break
                    
                    print(numbers, offset)
                    
                print(offset)
                
                if response_code == 0:
                    numbers1 = numbers[:midPoint]
                    numbers2 = numbers[midPoint:]
                    
                    print(numbers1, numbers2)
                            
                    if len(numbers1) != num_count or len(numbers2) != num_count:
                        print("Invalid input. Please enter the correct number of integers.")
                        response_code = 7
                    else:
                        print(f"Message Type: {msg_type}")
                        print(f"Message Length: {msg_length}")
                        print(f"Operation: {operation}")
                        print(f"Number Count: {num_count}")
                        print(f"Numbers1: {numbers1}")
                        print(f"Numbers2: {numbers2}")
                    
                        result  = add_number_sets(numbers1, numbers2)

        elif operation == 'E':
            conn.close()
            break

        else:
            print("Invalid operation")
            response_code = 1

        if response_code == 0:
            msg_type = 1
            
            if operation == 'A':
                msg = pack('!HBch', msg_type, response_code, operation.encode(), result)
            if operation == 'B':
                msg = pack('!HBcf', msg_type, response_code, operation.encode(), result)
            if operation == 'C':
                msg = pack('!HBc'+ 'I'*2, msg_type, response_code, operation.encode(), *result)
                
            conn.sendall(msg)
        
        else:
            msg_type = 1
            msg = pack('!HBc', msg_type, response_code, operation.encode())
            conn.sendall(msg)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive at port", str(serverPort))

    serverSocket.listen()
    ThreadCount=0
    while not close:
        
        conn, addr = serverSocket.accept()
        
        start_new_thread(thread_client, (conn, addr))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))


        if ThreadCount==5:
            serverSocket.close()

            
            
        
        