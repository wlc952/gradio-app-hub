import gradio as gr
import os
import sys
import psutil
import signal
import platform
from subprocess import Popen


system=platform.system()

def kill_process(pid):
    if(system=="Windows"):
        cmd = "taskkill /t /f /pid %s" % pid
        os.system(cmd)
    else:
        kill_proc_tree(pid)

def kill_proc_tree(pid, including_parent=True):  
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    children = parent.children(recursive=True)
    for child in children:
        try:
            os.kill(child.pid, signal.SIGTERM)  # or signal.SIGKILL
        except OSError:
            pass
    if including_parent:
        try:
            os.kill(parent.pid, signal.SIGTERM)  # or signal.SIGKILL
        except OSError:
            pass


class AppManager:
    def __init__(self):
        self.processes = {}
        self.ports = {}
        self.port = 5000

    def launch_app(self, app_name):
        try:
            if app_name in self.processes:
                print(f"{app_name} is already running on port {self.ports[app_name]}")
                return
            else:
                self.port += 1

                cmd = f'{sys.executable} apps/{app_name}.py --port {self.port}'
                p_process = Popen(cmd, shell=True)
                self.processes[app_name] = p_process
                self.ports[app_name] = self.port
                print(f"{app_name} launched on port {self.port}")
        except Exception as e:
            print(f"Failed to launch {app_name}: {e}")

    def shutdown_app(self, app_name):
        if app_name in self.processes:
            p_process = self.processes[app_name]
            kill_process(p_process.pid)
            del self.processes[app_name]
            del self.ports[app_name]
            print(f"{app_name} has been shut down")

def create_app_ui(app_manager):                    
    with gr.Blocks(title="Welcome to the AIGC App Store") as app_store:
        gr.Markdown("# Welcome to the AIGC App Store", elem_id="welcome_message")
        gr.HTML("""
        <style>
            #welcome_message {
                text-align: center;
            }
            .gr-tab {
                text-align: center;
            }
        </style>
        """)
        app_apis = []
        for x in os.listdir("apps"):
            if x.endswith(".py") and x != "__init__.py":
                app_apis.append(x.split(".")[0])
                
        def handle_launch(app_name):
            app_manager.launch_app(app_name)
            return gr.update(visible=False), gr.update(visible=True)

        def handle_shutdown(app_name):
            app_manager.shutdown_app(app_name)
            return gr.update(visible=True), gr.update(visible=False)
        
        for app_name in app_apis:
            with gr.Tab(app_name):
                app_module = __import__(f"apps.{app_name}", fromlist=['STANDALONE'])
                standalone = getattr(app_module, 'STANDALONE', False)
                if standalone:
                    launch_button = gr.Button("启动")
                    shutdown_button = gr.Button("关闭", visible=False)

                    launch_button.click(lambda app_name=app_name: handle_launch(app_name), outputs=[launch_button, shutdown_button])
                    shutdown_button.click(lambda app_name=app_name: handle_shutdown(app_name), outputs=[launch_button, shutdown_button])
    return app_store

if __name__ == "__main__":
    app_manager = AppManager()
    app_store = create_app_ui(app_manager)
    app_store.queue().launch(server_port=app_manager.port, inbrowser=True)