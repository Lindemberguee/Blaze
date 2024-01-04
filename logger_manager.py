import logging

class LoggerManager:
    def __init__(self, acerto_log_file="acerto.log", erramos_log_file="erramos.log", trend_log_file="trends.log"):
        self.acerto_log_file = acerto_log_file
        self.erramos_log_file = erramos_log_file
        self.trend_log_file = trend_log_file

        self.setup_loggers()

    def setup_loggers(self):
        # Configuração do logger para acertos
        self.acerto_logger = self.setup_logger("AcertoLogger", self.acerto_log_file)

        # Configuração do logger para erros
        self.erramos_logger = self.setup_logger("ErramosLogger", self.erramos_log_file)

        # Configuração do logger para registrar tendências
        self.trend_logger = self.setup_logger("TrendLogger", self.trend_log_file)

    def setup_logger(self, name, log_file):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def log_acerto(self, message):
        self.acerto_logger.info(message)

    def log_erro(self, message):
        self.erramos_logger.info(message)

    def log_trend(self, message):
        self.trend_logger.info(message)
