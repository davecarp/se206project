import os
import multiprocessing
import signal
import subprocess

class FestivalSlave(multiprocessing.Process):
    """
    Slave process for Festival.
    """
    def __init__(self, pipe, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self.pipe = pipe
        self.daemon = True

    def run(self):
        os.setsid()

        while True:
            text = self.pipe.recv()

            proc = subprocess.Popen([ "festival", "--tts" ], stdin=subprocess.PIPE)
            proc.stdin.write(text)
            proc.stdin.close()

class Festival(object):
    def start(self):
        """
        Start the Festival connector.
        """
        self.pipe, endpoint = multiprocessing.Pipe()
        self.proc = FestivalSlave(endpoint)
        self.proc.start()

    def speak(self, text):
        """
        Send the text to speak along the pipe to the slave.
        """
        self.pipe.send(text)

    def kill(self):
        """
        Kill the slave.
        """
        os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)

    def panic(self):
        """
        Kill the slave and restart it.
        """
        self.kill()
        self.start()
