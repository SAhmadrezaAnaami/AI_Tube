import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'message': record.getMessage(),
            'name': record.name,
            'timestamp': self.formatTime(record, self.datefmt),
        }
        return json.dumps(log_record, ensure_ascii=False)

def setup_json_logger(log_file, logger_name):
    logger = logging.getLogger(logger_name)  # Use unique logger name
    logger.setLevel(logging.DEBUG)
    
    # Ensure no duplicate handlers are added (to avoid logging duplication)
    if not logger.hasHandlers():
        # Add UTF-8 encoding to handle non-ASCII characters
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
    return logger
