import socket
import threading
import protobuf_messages_pb2 
import struct
import sys
import time
import random
import numpy as np
import os

def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))  
    public_ip = sock.getsockname()[0]
    sock.close()
    return public_ip



def main():
    multicast_group = "224.0.0.1"
    multicast_port = 54321
    DEVICE_HOST = get_public_ip()
    DEVICE_PORT = 8090
    global CONNECTED
    global SENDING
    SENDING = False
    CONNECTED = True

    # Criando um socket UDP para escutar o grupo multicast
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_socket.bind(("", multicast_port))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack("4sL", group, socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Dispositivo ouvindo em {multicast_group}:{multicast_port}")

    while True:
        data, addr = multicast_socket.recvfrom(1024)
        print("Endereço IP do remetente:", addr[0])
        discovery_message = protobuf_messages_pb2.Discovery()
        discovery_message.ParseFromString(data)

        # Adicionando um print para verificar a mensagem de descoberta
        print(f"Recebido: {discovery_message.message}")

        if discovery_message.message == "Descoberta de dispositivos: Quem está aí?":
            # criando um novo socket UDP de servidor para aguardar a conexão do Gateway
            server_socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            server_socket_receive.bind((DEVICE_HOST, DEVICE_PORT))

            # Criando uma mensagem de identificação usando Protocol Buffers
            identification_message = protobuf_messages_pb2.Identification()
            identification_message.device_type = "Sensor de Temperatura"
            identification_message.device_ip = DEVICE_HOST
            identification_message.device_port = DEVICE_PORT
            identification_message.protocol = "UDP"  

            # Adicionando um print para verificar a mensagem de identificação
            print(f"Enviado: {identification_message}")

            # Enviando a mensagem de identificação para o gateway
            multicast_socket.sendto(identification_message.SerializeToString(), addr)

            gateway_port_data = server_socket_receive.recv(1024)
            gateway_port_message = protobuf_messages_pb2.GatewayPort()
            gateway_port_message.ParseFromString(gateway_port_data)

            gateway_port = gateway_port_message.gateway_port
            
            print(f"Dispositivo enviando para o endereço {addr[1]}:{gateway_port}")
            
            def receive_data():
                global CONNECTED
                global SENDING

                while CONNECTED:
                    response_data = server_socket_receive.recv(1024)
                    response = protobuf_messages_pb2.GatewayToDeviceMessage()
                    response.ParseFromString(response_data)

                    print(response.command)

                    if response.command == "Desligue":
                        CONNECTED = False
                        multicast_socket.close()
                        server_socket_receive.close()
                        server_socket_send.close()
                        os._exit(0) 

                    elif response.command == "Iniciar":
                        SENDING = True

                    elif response.command == "Pare":
                        SENDING = False

            def send_data():
                global CONNECTED
                global SENDING
                while CONNECTED: 
                    while SENDING:
                        # Simulação de leitura de umidade do solo (envio contínuo)
                        temperature_data = read_temperature_data()  # Função para simular a leitura de temperatura
                        print(temperature_data)
                        server_socket_send.sendto(temperature_data.SerializeToString(), (addr[0], gateway_port))

                        time.sleep(4)

            # Criando threads para recepção e envio
            receive_thread = threading.Thread(target=receive_data)
            send_thread = threading.Thread(target=send_data)

            # Iniciando as threads
            receive_thread.start()
            send_thread.start()


def read_temperature_data():
    temperature_message = protobuf_messages_pb2.DeviceToGatewayMessage()
    mean_temperature = 25.0  # Média de temperatura
    std_deviation = 2.0      # Desvio padrão da temperatura

    temperature_value = round(np.random.normal(mean_temperature, std_deviation), 1)
    temperature_message.response = f"{temperature_value}°C"
    return temperature_message

if __name__ == "__main__":
    main()


