import sys
import os
from datetime import datetime

# Базовые имена файлов (без пути)
VERSION_FILE_NAME = 'version'
VERSION_LOG_FILE_NAME = 'version_log'
LOGS_FILE_NAME = 'logs'

class VersionManager:
    def __init__(self, base_path):
    # Проверяем, что путь существует и доступен для чтения
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Path {base_path} does not exist")
    
    if not os.access(base_path, os.R_OK | os.W_OK):
        raise PermissionError(f"No write permissions for {base_path}")
    
    self.base_path = base_path
    self.version_file = os.path.join(base_path, 'version')
    self.version_log_file = os.path.join(base_path, 'version_log')
        
        # Создаем директорию, если ее нет
        # os.makedirs(base_path, exist_ok=True)

    def get_current_timestamp(self):
        now = datetime.now()
        return now.strftime('%d.%m.%Y %H:%M:%S.') + f'{now.microsecond // 1000:03d}'

    def read_current_version(self):
        try:
            with open(self.version_file, 'r') as f:
                version = f.read().strip()
                if not version:
                    raise ValueError("Version file is empty")
                
                parts = version.split('.')
                if len(parts) != 3 or not all(p.isdigit() for p in parts):
                    raise ValueError("Invalid version format")
                
                return version
        except (FileNotFoundError, ValueError):
            # Если файла нет или он некорректен, создаем версию по умолчанию
            default_version = '0.0.1'
            self.write_version(default_version)
            return default_version

    def write_version(self, version):
        with open(self.version_file, 'w') as f:
            f.write(version)

    def get_last_log_message(self):
        try:
            if not os.path.exists(self.version_log_file):
                return "No version log available"
            
            with open(self.version_log_file, 'r') as f:
                first_line = f.readline().strip()
                if not first_line:
                    return "Empty version log"
                
                # Извлекаем сообщение после последнего ']'
                parts = first_line.split(']')
                return parts[-1].strip() if len(parts) > 1 else first_line
        except Exception as e:
            print(f"Error reading version log: {str(e)}", file=sys.stderr)
            return "Error reading version log"

    def prepend_to_file(self, filename, content):
        existing = ''
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = f.read().strip('\n')
        with open(filename, 'w') as f:
            f.write(content)
            if existing:
                f.write('\n' + existing)

def main():
    if len(sys.argv) < 3:
        print("Usage: python version_up.py <version_dir_path> <command>")
        sys.exit(1)
        
    version_dir = sys.argv[1]
    command = sys.argv[2]
    
    version_file = os.path.join(version_dir, 'version')
    version_log_file = os.path.join(version_dir, 'version_log')
    
    if not os.path.exists(version_file):
        print(f"Error: Version file not found at {version_file}")
        sys.exit(1)

if __name__ == '__main__':
    main()







# import sys
# import os
# from datetime import datetime

# # Инициализация путей к файлам (будут переопределены в change_path_to_files)
# VERSION_FILE = 'version'
# VERSION_LOG_FILE = 'version_log'
# LOGS_FILE = 'logs'

# def get_current_timestamp():
#     """Возвращает текущее время в формате 'дд.мм.гггг чч:мм:сс.мс'"""
#     now = datetime.now()
#     return now.strftime('%d.%m.%Y %H:%M:%S.') + f'{now.microsecond // 1000:03d}'

# def prepend_to_file(filename, content):
#     """Добавляет строку в начало файла"""
#     existing = ''
#     if os.path.exists(filename):
#         with open(filename, 'r') as f:
#             existing = f.read().strip('\n')
#     with open(filename, 'w') as f:
#         f.write(content)
#         if existing:
#             f.write('\n' + existing)

# def read_current_version():
#     """Читает текущую версию из файла"""
#     try:
#         with open(VERSION_FILE, 'r') as f:
#             version = f.read().strip()
#             if not version:
#                 raise ValueError("Файл версии пуст.")
#             parts = version.split('.')
#             if len(parts) != 3 or not all(p.isdigit() for p in parts):
#                 raise ValueError("Неверный формат версии.")
#             return version
#     except (FileNotFoundError, ValueError):
#         default_version = '0.0.1'
#         write_version(default_version)
#         return default_version

# def write_version(version):
#     """Записывает версию в файл"""
#     with open(VERSION_FILE, 'w') as f:
#         f.write(version)

# def print_version():
#     """Выводит текущую версию"""
#     print(read_current_version())

# def print_help():
#     """Выводит справку по командам"""
#     help_text = """Доступные команды:
#     version          - Показать текущую версию
#     patch            - Увеличить версию патча (0.0.x)
#     minor            - Увеличить минорную версию (0.x.0)
#     major            - Увеличить мажорную версию (x.0.0)
#     drop             - Сбросить версию до 0.0.1 и очистить все логи
#     clear            - Очистить логи команд
#     undo             - Откат предыдущего действия
#     version_log      - Показать логи смены версий (используйте -n для вывода n записей)
#     log              - Показать все логи (используйте -n для вывода n записей)
#     get_last_log_msg - Получить последнее сообщение из лога версий"""
#     print(help_text)

# def update_version(update_type):
#     """Обновляет версию согласно типу обновления"""
#     current = read_current_version()
#     major, minor, patch = map(int, current.split('.'))
    
#     if update_type == 'patch':
#         patch += 1
#     elif update_type == 'minor':
#         minor += 1
#         patch = 0
#     elif update_type == 'major':
#         major += 1
#         minor = 0
#         patch = 0
    
#     new_version = f'{major}.{minor}.{patch}'
#     write_version(new_version)
#     timestamp = get_current_timestamp()
#     log_entry = f'[{new_version}] <- [{current}] [{timestamp}] {update_type} update'
#     prepend_to_file(VERSION_LOG_FILE, log_entry)
#     print(f"Версия обновлена до {new_version}")

# def drop_version():
#     """Сбрасывает версию и очищает логи"""
#     write_version('0.0.1')
#     open(VERSION_LOG_FILE, 'w').close()
#     open(LOGS_FILE, 'w').close()
#     print("Версия сброшена до 0.0.1, все логи очищены.")

# def clear_logs():
#     """Очищает логи команд"""
#     open(LOGS_FILE, 'w').close()
#     print("Логи команд очищены.")

# def undo_version():
#     """Откатывает версию к предыдущей"""
#     try:
#         with open(VERSION_LOG_FILE, 'r') as f:
#             lines = f.readlines()
#             if not lines:
#                 print("Ошибка: Лог версий пуст.")
#                 return
#             latest_line = lines[0].strip()
#     except FileNotFoundError:
#         print("Ошибка: Лог версий пуст.")
#         return
    
#     parts = latest_line.split(' <- ')
#     if len(parts) != 2:
#         print("Ошибка: Неверный формат записи в логе.")
#         return
    
#     new_part, rest = parts
#     new_version = new_part[1:-1]
#     old_part = rest.split('] [', 1)[0]
#     old_version = old_part[1:]
#     current = read_current_version()
    
#     if current != new_version:
#         print(f"Ошибка: Текущая версия {current} не совпадает с записью в логе {new_version}.")
#         return
    
#     write_version(old_version)
#     timestamp = get_current_timestamp()
#     log_entry = f'[{old_version}] <- [{new_version}] [{timestamp}] undo'
#     prepend_to_file(VERSION_LOG_FILE, log_entry)
#     print(f"Версия откачена до {old_version}")

# def show_version_log(n=None):
#     """Выводит логи смены версий"""
#     try:
#         with open(VERSION_LOG_FILE, 'r') as f:
#             lines = [line.strip() for line in f.readlines() if line.strip()]
#             if not lines:
#                 print("Лог версий пуст.")
#                 return
#             if n is not None:
#                 lines = lines[:n]
#             for line in lines:
#                 print(line)
#     except FileNotFoundError:
#         print("Лог версий пуст.")

# def show_logs(n=None):
#     """Выводит все логи"""
#     try:
#         with open(LOGS_FILE, 'r') as f:
#             lines = [line.strip() for line in f.readlines() if line.strip()]
#             if not lines:
#                 print("Логи пусты.")
#                 return
#             if n is not None:
#                 lines = lines[:n]
#             for line in lines:
#                 print(line)
#     except FileNotFoundError:
#         print("Логи пусты.")

# def get_last_log_msg(version_file_path):
#     """Получает последнее сообщение из лога версий"""
#     try:
#         log_dir = os.path.dirname(version_file_path)
#         log_file = os.path.join(log_dir, 'version_log')
        
#         if os.path.exists(log_file):
#             with open(log_file, 'r') as f:
#                 first_line = f.readline().strip()
#                 if first_line:
#                     # Возвращаем часть после последнего ]
#                     return first_line.split(']')[-1].strip()
#         return "No version log available"
#     except Exception as e:
#         print(f"Error reading log: {str(e)}", file=sys.stderr)
#         return "Error reading log"

# def change_path_to_files(absolut_path):
#     """Изменяет пути к файлам данных"""
#     global VERSION_FILE, VERSION_LOG_FILE, LOGS_FILE
#     os.makedirs(absolut_path, exist_ok=True)
#     VERSION_FILE = os.path.join(absolut_path, 'version')
#     VERSION_LOG_FILE = os.path.join(absolut_path, 'version_log')
#     LOGS_FILE = os.path.join(absolut_path, 'logs')

# def main():
#     if len(sys.argv) < 3:
#         print("Ошибка: Недостаточно аргументов. Используйте 'help' для справки.")
#         sys.exit(1)
    
#     path = sys.argv[1]
#     command = sys.argv[2]
    
#     # Инициализация путей к файлам
#     change_path_to_files(os.path.dirname(path))
    
#     # Специальная команда для получения последнего сообщения лога
#     if command == "get_last_log_msg":
#         print(get_last_log_msg(path))
#         return
    
#     # Логирование вызова команды
#     timestamp = get_current_timestamp()
#     log_entry = ' '.join(sys.argv[1:])
    
#     if command != "log":
#         prepend_to_file(LOGS_FILE, f'[{timestamp}] {log_entry}')
    
#     # Обработка команд
#     if command == 'version':
#         print_version()
#     elif command == 'help':
#         print_help()
#     elif command in ('patch', 'minor', 'major'):
#         update_version(command)
#     elif command == 'drop':
#         drop_version()
#     elif command == 'clear':
#         clear_logs()
#     elif command == 'undo':
#         undo_version()
#     elif command == 'version_log':
#         n = None
#         if len(sys.argv) >= 4 and sys.argv[3].startswith('-'):
#             try:
#                 n = int(sys.argv[3][1:])
#             except ValueError:
#                 print("Ошибка: Неверное число после флага.")
#                 sys.exit(1)
#         show_version_log(n)
#     elif command == 'log':
#         n = None
#         if len(sys.argv) >= 4 and sys.argv[3].startswith('-'):
#             try:
#                 n = int(sys.argv[3][1:])
#             except ValueError:
#                 print("Ошибка: Неверное число после флага.")
#                 sys.exit(1)
#         show_logs(n)
#     else:
#         print(f"Ошибка: Неизвестная команда '{command}'. Используйте 'help' для справки.")
#         sys.exit(1)

# if __name__ == '__main__':
#     main()
