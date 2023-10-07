import logging

class MyLogger:
    def __init__(self, name: str='my_logger', log_level: int=logging.DEBUG, log_file: str | None=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.log_format = logging.Formatter('[%(levelname)s] %(asctime)s: %(name)s %(module)s %(funcName)s:%(lineno)d - "%(message)s"')
        # Создаем обработчик для вывода лога в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.log_format)
        self.logger.addHandler(console_handler)
        
        # Если указан файл для логирования, создаем обработчик для записи в файл
        if log_file:
            self.add_file_handler(log_file)
    
    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)
    
    def add_file_handler(self, log_file):
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(self.log_format)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger
    
if __name__ == "__main__":
    logger = MyLogger().get_logger()
    logger.info("starting app")
    