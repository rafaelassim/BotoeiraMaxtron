import threading
import time

class PeriodicFunction:
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.lock = threading.Lock()
        self.timer = None
        self.running = True
        self.start_timer()

    def start_timer(self):
        """Inicia ou reinicia o temporizador."""
        with self.lock:
            if not self.running:
                return
            if self.timer:
                self.timer.cancel()  # Cancela qualquer temporizador ativo
            self.timer = threading.Timer(self.interval, self.run)
            self.timer.start()

    def run(self):
        """Executa a função e reinicia o temporizador se estiver ativo."""
        with self.lock:
            if not self.running:
                return
        self.function()
        self.start_timer()  # Continua o loop periódico

    def trigger_now(self):
        """Executa a função imediatamente e reinicia o temporizador corretamente."""
        with self.lock:
            if not self.running:
                return
            if self.timer:
                self.timer.cancel()  # Cancela o temporizador atual
        self.function()  # Executa a função imediatamente
        self.start_timer()  # Reinicia o ciclo periódico

    def stop(self):
        """Para o temporizador."""
        with self.lock:
            self.running = False
            if self.timer:
                self.timer.cancel()
                self.timer = None

# Exemplo de uso
#def minha_funcao():
#    print(f"Função executada em {time.strftime('%H:%M:%S')}")

# Criando o objeto com um intervalo de 5 segundos
#pf = PeriodicFunction(1, minha_funcao)

# Aguarda um pouco e aciona manualmente
#time.sleep(10)
#print("Chamando manualmente...")
#pf.trigger_now()

# Aguarda mais um pouco antes de parar
#time.sleep(10)
#pf.stop()
#print("Temporizador parado.")
