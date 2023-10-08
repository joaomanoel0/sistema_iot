import socket
import threading
import protobuf_messages_pb2
import struct
import sys

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
    DEVICE_PORT = 8083
    STATUS_water_pump = False #False = apagada e True = acesa

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
        discovery_message = protobuf_messages_pb2.Discovery()
        discovery_message.ParseFromString(data)


        # Adicionando um print para verificar a mensagem de descoberta
        print(f"Recebido: {discovery_message.message}")

        if discovery_message.message == "Descoberta de dispositivos: Quem está aí?":

            # criando um novo socket TCP para a comunicação direta com o Gateway
            device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

            try:
                device_socket.bind((DEVICE_HOST, DEVICE_PORT))
            except socket.error:
                print("Não foi possível estabelecer conexão com o socket. Encerrando servidor.")
                sys.exit(0)

            # Criando uma mensagem de identificação usando Protocol Buffers
            identification_message = protobuf_messages_pb2.Identification()
            identification_message.device_type = "Bomba d'agua"  # Substitua pelo tipo do dispositivo
            identification_message.device_ip = DEVICE_HOST  # Substitua pelo IP do dispositivo
            identification_message.device_port = DEVICE_PORT  # Substitua pela porta do dispositivo
            identification_message.protocol = "TCP"

            # Adicionando um print para verificar a mensagem de identificação
            print(f"Enviado: {identification_message}")

            # Enviando a mensagem de identificação de volta ao endereço de origem da mensagem de descoberta
            multicast_socket.sendto(identification_message.SerializeToString(), addr)           
           

            device_socket.listen(1)

            print(f"Dispositivo iniciado no endereço {DEVICE_HOST}:{DEVICE_PORT}")
            print("Aguardando conexão ...")

            while True:
                try:
                    client_socket, client_address = device_socket.accept()
                    print(f"Conexão estabelecida com {client_address}")
                    while True:
                        # Lógica do dispositivo - Importante tratar uma mensagem /MENU enviando o menu ao usuário. E tratar os outros comandos
                        data = client_socket.recv(1024)
                        gateway_message = protobuf_messages_pb2.GatewayToDeviceMessage()
                        gateway_message.ParseFromString(data)

                        user_command = gateway_message.command
                        print(user_command)

                        response_message = protobuf_messages_pb2.DeviceToGatewayMessage()

                        if user_command == "/Menu":
                            response_message.response = "Digite:\n1 - Para ligar a bomba\n2 - Para desligar a bomba\n3 - Para ver o status da bomba"
                        elif user_command == "1":
                            if STATUS_water_pump:
                                response_message.response = "Bomba já está ligada"
                            else:
                                STATUS_water_pump = True
                                response_message.response = "Bomba foi ligada"
                        elif user_command == "2":
                            if STATUS_water_pump:
                                STATUS_water_pump = False
                                response_message.response = "Bomba foi desligada"
                            else:
                                response_message.response = "Bomba já está desligada"
                        elif user_command =='3':
                            response_message.response="Bomba está ligada" if STATUS_water_pump else "Bomba está desligada"
                        else:
                             response_message.response = "Comando inválido: Digite /Menu para ver os comandos do dispositivo"

                        client_socket.send(response_message.SerializeToString())

                except OSError as e:
                    print("Conexão com o gateway perdida")
                    sys.exit(0)
                    break


if __name__ == "__main__":
    main()




