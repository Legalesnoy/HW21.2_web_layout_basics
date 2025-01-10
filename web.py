# Импорт встроенной библиотеки для работы веб-сервера
import re
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    base_dir = os.path.join(os.getcwd(), 'html')
    content_type = {'.css':'text/css',
                    '.js':'application/javascript',
                    '.png':'image/png',
                    '.jpg':'image/jpeg',
                    '.jpeg':'image/jpeg',
                    '.html':"text/html"
                    }

    def get_data(self, filename):
        try:
            with open(filename,'r',encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def do_GET(self):
        path = self.path
        if path == '/':
            path = '/main.html'
        file_path = os.path.join(self.base_dir, path.lstrip('/'))
        content_type = self.content_type.get(file_path.endswith, 'text/html')

        data = self.get_data(file_path)


        if data is not None:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/submit-form':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            data = {}
            for pair in post_data.split('&'):
                key, value = pair.split('=')
                data[key] = value


            name = data.get('name', '')
            email = data.get('email', '')
            message = data.get('message', '')

            name = re.sub(r'%([0-9A-Fa-f]{2})|\\+', lambda m: chr(int(m.group(1), 16)) if m.group(1) else ' ', name)
            email = re.sub(r'%([0-9A-Fa-f]{2})|\\+', lambda m: chr(int(m.group(1), 16)) if m.group(1) else ' ', email)
            message = re.sub(r'%([0-9A-Fa-f]{2})|\\+', lambda m: chr(int(m.group(1), 16)) if m.group(1) else ' ', message)

            print(f"Получено сообщение от {name} ({email}): {message}")


            self.send_response(303)
            self.send_header("Location", "/contacts.html")
            self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f'Server started http://{hostName}:{serverPort}')

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")