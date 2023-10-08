import socket
import threading
import protobuf_messages_pb2  
import time
import sys
import select
import random


def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))  
    public_ip = sock.getsockname()[0]
    sock.close()
    return public_ip

gateway_udp_port = 8081

gateway_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_udp_socket.bind((get_public_ip(), gateway_udp_port))

# Função para mover o cursor para a posição desejada
def move_cursor(x, y):
    print(f"\x1b[{y};{x}H", end="")  # Usando códigos ANSI para mover o cursor


class Device:
    def __init__(self, device_type, device_ip, device_port, protocol, socket=None):
        self.device_type = device_type
        self.device_ip = device_ip
        self.device_port = device_port
        self.socket = socket
        self.protocol = protocol

    def send_command(self, command):
        try:
            message = protobuf_messages_pb2.GatewayToDeviceMessage()
            message.command = command
            self.socket.send(message.SerializeToString())

            response_data = self.socket.recv(1024)
            response = protobuf_messages_pb2.DeviceToGatewayMessage()
            response.ParseFromString(response_data)

            return response.response
        except Exception as e:
            return str(e)

class Gateway:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected_devices = []

    def start(self):
        self.discover_devices()
        self.start_cli()

    def handle_device(self, device_type, device_ip, device_port, protocol):
        if protocol == "TCP":
            device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                device_socket.connect((device_ip, device_port))
            except socket.error:
                print(f"Não foi possível se conectar ao dispositivo {device_type}")
                return
            device = Device(device_type, device_ip, device_port, protocol, device_socket)
        elif protocol == "UDP":
            message = protobuf_messages_pb2.GatewayPort()
            message.gateway_port = gateway_udp_port  
            serialized_message = message.SerializeToString()
            gateway_udp_socket.sendto(serialized_message, (device_ip, device_port))
            device = Device(device_type, device_ip, device_port, protocol)
        else:
            print(f"Protocolo {protocol} não suportado. Ignorando dispositivo {device_type}")
            return

        self.connected_devices.append(device)

    def discover_devices(self):
        timeout = 5
        print("Descobrindo dispositivos...")
        discovery_message = protobuf_messages_pb2.Discovery()
        discovery_message.message = "Descoberta de dispositivos: Quem está aí?"

        multicast_group = ("224.0.0.1", 54321)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as multicast_socket:
            multicast_socket.sendto(discovery_message.SerializeToString(), multicast_group)

            try:
                multicast_socket.settimeout(timeout)

                while True:
                    data, _ = multicast_socket.recvfrom(1024)
                    identification_message = protobuf_messages_pb2.Identification()
                    identification_message.ParseFromString(data)
                    

                    if all([identification_message.device_type, identification_message.device_ip,
                            identification_message.device_port, identification_message.protocol]):
                        device_type = identification_message.device_type
                        device_ip = identification_message.device_ip
                        device_port = identification_message.device_port
                        protocol = identification_message.protocol

                        device_thread = threading.Thread(target=self.handle_device,
                                                        args=(device_type, device_ip, device_port, protocol))
                        device_thread.start()

            except socket.timeout:
                print("Tempo limite de descoberta expirado. Iniciando a interface de linha de comando.")

    def start_cli(self):
        while True:
            print("Escolha o dispositivo:")
            for idx, device in enumerate(self.connected_devices):
                print(f"{idx + 1}. {device.device_type}")

            choice = input("Digite o número do dispositivo ou /VOLTAR para sair: ")

            if choice == "/VOLTAR":
                break

            try:
                choice = int(choice)
                if 1 <= choice <= len(self.connected_devices):
                    device = self.connected_devices[choice - 1]

                    if device.protocol == "UDP":
                        print("Pressione 'Q' a qualquer momento para voltar ao menu principal.")
                        print(f"Recebendo mensagens do dispositivo {device.device_type} ")
                        message = protobuf_messages_pb2.GatewayToDeviceMessage()
                        message.command = "Iniciar"
                        gateway_udp_socket.sendto(message.SerializeToString(), (device.device_ip, device.device_port))
                        last_addr = None
                        first_message_printed = False
                        while True:
                            data, addr = gateway_udp_socket.recvfrom(1024)
                            message = f"Recebido de {device.device_type}: {data.decode()}"
                            
                            # Movendo o cursor para a primeira posição da linha anterior
                            if last_addr:
                                move_cursor(0, last_addr[1] + 1)
                            if not first_message_printed:
                                print(message)
                                first_message_printed = True
                            else:
                            # Limpando as duas linhas anteriores
                                print("\033[F\033[K\033[F\033[K", end="")
                                print(message)
                            last_addr = addr
                            # Verificando continuamente se o usuário pressionou 'Q' para sair
                            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                                user_input = input()
                                if user_input == 'Q':
                                    break

                        message = protobuf_messages_pb2.GatewayToDeviceMessage()
                        message.command = "Pare"
                        gateway_udp_socket.sendto(message.SerializeToString(), (device.device_ip, device.device_port))

                    else:
                        menu = device.send_command("/Menu")
                        print(menu)
                        while True:
                            user_command = input(f"Digite um comando para o dispositivo({device.device_type}) ou /VOLTAR: ")
                            if not user_command:
                                continue

                            elif user_command == "/VOLTAR":
                                break
                            # Enviar o comando para o dispositivo e receber a resposta, se necessário
                            response = device.send_command(user_command)
                            print(response)
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite o número do dispositivo ou /VOLTAR.")
 


if __name__ == "__main__":
    gateway = Gateway("127.0.0.1", 12345)
    print("Procurando dispositivos, aguarde 5 segundos")
    gateway.start()


for device in gateway.connected_devices:
    if device.protocol == "UDP":
        message = protobuf_messages_pb2.GatewayToDeviceMessage()
        message.command = "Pare"
        gateway_udp_socket.sendto(message.SerializeToString(), (device.device_ip, device.device_port))











