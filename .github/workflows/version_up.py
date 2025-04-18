import os
import sys
from datetime import datetime


def format_version(version_list):
    if len(version_list) == 0:
        return ""
    return f"{version_list[0]}.{version_list[1]}.{version_list[2]}"


def get_version(version_catalog) -> list[int]:
    version = []
    version_file_name = f"{version_catalog}/version"
    if not os.path.exists(version_file_name):
        open(version_file_name, "x").close()
    with open(version_file_name, "r") as f:
        lines = f.readlines()

        if len(lines) == 0:
            return [0, 0, 0]

        for i, line in enumerate(lines):
            if i > 2: break
            version.append(int(line.split(' ')[1]))

    return version


def get_message():
    try:
        msg = sys.argv[4]
    except IndexError as e:
        return "No message"

    return msg


def upgrade_version(version_type, version_catalog):
    old_version_list = get_version(version_catalog)

    if old_version_list == [0, 0, 0]:
        log_version_into_file([1, 0, 0], [], "Initial version", version_catalog)
        write_version_into_file([1, 0, 0], version_catalog)
        return

    new_version_list = old_version_list.copy()

    if version_type == "major":
        new_version_list[0] = new_version_list[0] + 1
        new_version_list[1] = 0
        new_version_list[2] = 0
    elif version_type == "minor":
        new_version_list[1] = new_version_list[1] + 1
        new_version_list[2] = 0
    elif version_type == "patch":
        new_version_list[2] = new_version_list[2] + 1
    else:
        raise ValueError("No such version type: " + version_type)

    write_version_into_file(new_version_list, version_catalog)
    message = get_message()
    log_version_into_file(new_version_list, old_version_list, message, version_catalog)
    print(f"Version updated: {format_version(old_version_list)} -> {format_version(new_version_list)}")


def write_version_into_file(version_list, version_catalog):
    with open(f"{version_catalog}/version.txt", "w") as f:
        f.write(f"major: {version_list[0]}\n")
        f.write(f"minor: {version_list[1]}\n")
        f.write(f"patch: {version_list[2]}\n")
        f.write(f"version: {format_version(version_list)}")


def log_version_into_file(new_version, old_version, message, version_catalog):
    with open(f"{version_catalog}/version_log.txt", "a") as f:
        f.write(
            f"[{format_version(new_version)} <- {format_version(old_version)}] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] | {message}\n")


def get_last_log_msg_from_file(version_catalog):
    version_file = f"{version_catalog}/version_log.txt"
    if not os.path.exists(version_catalog):
        os.makedirs(version_catalog, exist_ok=True)
    if not os.path.exists(version_file):
        with open(version_file, "w") as f:
            f.write("Initial version\n")
        return "Initial version"
    
    with open(version_file, "r") as f:
        lines = f.readlines()
        if not lines:
            return "No messages yet"
        last_line = lines[-1].strip()
        if not last_line:
            return "No messages yet"
        if '|' in last_line:
            return last_line.split('|')[1].strip()
        return last_line
    

def is_file_exists(filename):
    return os.path.isfile(filename)


def get_args_map():
    args_len = len(sys.argv)
    if args_len < 2:
        raise ValueError('Please, provide at least two arguments: catalog and version type')

    args_map = {}
    args_map['catalog'] = sys.argv[1]
    args_map['command_type'] = sys.argv[2]
    
    if args_map['command_type'] == 'upgrade_version':
        args_map['version_type'] = sys.argv[3]

    return args_map


args_map = get_args_map()
command_type = args_map['command_type']
version_catalog = args_map['catalog']

if command_type == 'get_current_version':
    print(format_version(get_version(version_catalog)))
elif command_type == 'get_last_log_msg':
    print(get_last_log_msg_from_file(version_catalog))
elif command_type == 'upgrade_version':
    version_type = args_map['version_type']
    upgrade_version(version_type, version_catalog)
else:
    raise ValueError("Unknow command type: " + command_type)













# import sys
# import os
# from datetime import datetime

# class VersionManager:
#     def __init__(self, base_path):
#         if not os.path.exists(base_path):
#             raise FileNotFoundError(f"Path {base_path} does not exist")
        
#         self.base_path = base_path
#         self.version_file = os.path.join(base_path, 'version')
#         self.version_log_file = os.path.join(base_path, 'version_log')
#         self.logs_file = os.path.join(base_path, 'logs')

#     def get_current_timestamp(self):
#         now = datetime.now()
#         return now.strftime('%d.%m.%Y %H:%M:%S.') + f'{now.microsecond // 1000:03d}'

#     def read_current_version(self):
#         try:
#             with open(self.version_file, 'r') as f:
#                 version = f.read().strip()
#                 if not version:
#                     raise ValueError("Version file is empty")
#                 return version
#         except Exception as e:
#             print(f"Error reading version: {str(e)}", file=sys.stderr)
#             return "0.0.1"

#     def get_last_log_message(self):
#         try:
#             if not os.path.exists(self.version_log_file):
#                 return "No version log available"
            
#             with open(self.version_log_file, 'r') as f:
#                 first_line = f.readline().strip()
#                 if not first_line:
#                     return "Empty version log"
                
#                 parts = first_line.split(']')
#                 return parts[-1].strip() if len(parts) > 1 else first_line
#         except Exception as e:
#             print(f"Error reading log: {str(e)}", file=sys.stderr)
#             return "Error reading version log"

# def main():
#     if len(sys.argv) < 3:
#         print("Usage: python version_up.py <path> <command>")
#         sys.exit(1)

#     path = sys.argv[1]
#     command = sys.argv[2]
    
#     try:
#         manager = VersionManager(path)
        
#         if command == "get_current_version":
#             print(manager.read_current_version())
#         elif command == "get_last_log_msg":
#             print(manager.get_last_log_message())
#         else:
#             print(f"Unknown command: {command}", file=sys.stderr)
#             sys.exit(1)
#     except Exception as e:
#         print(f"Error: {str(e)}", file=sys.stderr)
#         sys.exit(1)

# if __name__ == '__main__':
#     main()







# # import sys
# # import os
# # from datetime import datetime

# # # Инициализация путей к файлам (будут переопределены в change_path_to_files)
# # VERSION_FILE = 'version'
# # VERSION_LOG_FILE = 'version_log'
# # LOGS_FILE = 'logs'

# # def get_current_timestamp():
# #     """Возвращает текущее время в формате 'дд.мм.гггг чч:мм:сс.мс'"""
# #     now = datetime.now()
# #     return now.strftime('%d.%m.%Y %H:%M:%S.') + f'{now.microsecond // 1000:03d}'

# # def prepend_to_file(filename, content):
# #     """Добавляет строку в начало файла"""
# #     existing = ''
# #     if os.path.exists(filename):
# #         with open(filename, 'r') as f:
# #             existing = f.read().strip('\n')
# #     with open(filename, 'w') as f:
# #         f.write(content)
# #         if existing:
# #             f.write('\n' + existing)

# # def read_current_version():
# #     """Читает текущую версию из файла"""
# #     try:
# #         with open(VERSION_FILE, 'r') as f:
# #             version = f.read().strip()
# #             if not version:
# #                 raise ValueError("Файл версии пуст.")
# #             parts = version.split('.')
# #             if len(parts) != 3 or not all(p.isdigit() for p in parts):
# #                 raise ValueError("Неверный формат версии.")
# #             return version
# #     except (FileNotFoundError, ValueError):
# #         default_version = '0.0.1'
# #         write_version(default_version)
# #         return default_version

# # def write_version(version):
# #     """Записывает версию в файл"""
# #     with open(VERSION_FILE, 'w') as f:
# #         f.write(version)

# # def print_version():
# #     """Выводит текущую версию"""
# #     print(read_current_version())

# # def print_help():
# #     """Выводит справку по командам"""
# #     help_text = """Доступные команды:
# #     version          - Показать текущую версию
# #     patch            - Увеличить версию патча (0.0.x)
# #     minor            - Увеличить минорную версию (0.x.0)
# #     major            - Увеличить мажорную версию (x.0.0)
# #     drop             - Сбросить версию до 0.0.1 и очистить все логи
# #     clear            - Очистить логи команд
# #     undo             - Откат предыдущего действия
# #     version_log      - Показать логи смены версий (используйте -n для вывода n записей)
# #     log              - Показать все логи (используйте -n для вывода n записей)
# #     get_last_log_msg - Получить последнее сообщение из лога версий"""
# #     print(help_text)

# # def update_version(update_type):
# #     """Обновляет версию согласно типу обновления"""
# #     current = read_current_version()
# #     major, minor, patch = map(int, current.split('.'))
    
# #     if update_type == 'patch':
# #         patch += 1
# #     elif update_type == 'minor':
# #         minor += 1
# #         patch = 0
# #     elif update_type == 'major':
# #         major += 1
# #         minor = 0
# #         patch = 0
    
# #     new_version = f'{major}.{minor}.{patch}'
# #     write_version(new_version)
# #     timestamp = get_current_timestamp()
# #     log_entry = f'[{new_version}] <- [{current}] [{timestamp}] {update_type} update'
# #     prepend_to_file(VERSION_LOG_FILE, log_entry)
# #     print(f"Версия обновлена до {new_version}")

# # def drop_version():
# #     """Сбрасывает версию и очищает логи"""
# #     write_version('0.0.1')
# #     open(VERSION_LOG_FILE, 'w').close()
# #     open(LOGS_FILE, 'w').close()
# #     print("Версия сброшена до 0.0.1, все логи очищены.")

# # def clear_logs():
# #     """Очищает логи команд"""
# #     open(LOGS_FILE, 'w').close()
# #     print("Логи команд очищены.")

# # def undo_version():
# #     """Откатывает версию к предыдущей"""
# #     try:
# #         with open(VERSION_LOG_FILE, 'r') as f:
# #             lines = f.readlines()
# #             if not lines:
# #                 print("Ошибка: Лог версий пуст.")
# #                 return
# #             latest_line = lines[0].strip()
# #     except FileNotFoundError:
# #         print("Ошибка: Лог версий пуст.")
# #         return
    
# #     parts = latest_line.split(' <- ')
# #     if len(parts) != 2:
# #         print("Ошибка: Неверный формат записи в логе.")
# #         return
    
# #     new_part, rest = parts
# #     new_version = new_part[1:-1]
# #     old_part = rest.split('] [', 1)[0]
# #     old_version = old_part[1:]
# #     current = read_current_version()
    
# #     if current != new_version:
# #         print(f"Ошибка: Текущая версия {current} не совпадает с записью в логе {new_version}.")
# #         return
    
# #     write_version(old_version)
# #     timestamp = get_current_timestamp()
# #     log_entry = f'[{old_version}] <- [{new_version}] [{timestamp}] undo'
# #     prepend_to_file(VERSION_LOG_FILE, log_entry)
# #     print(f"Версия откачена до {old_version}")

# # def show_version_log(n=None):
# #     """Выводит логи смены версий"""
# #     try:
# #         with open(VERSION_LOG_FILE, 'r') as f:
# #             lines = [line.strip() for line in f.readlines() if line.strip()]
# #             if not lines:
# #                 print("Лог версий пуст.")
# #                 return
# #             if n is not None:
# #                 lines = lines[:n]
# #             for line in lines:
# #                 print(line)
# #     except FileNotFoundError:
# #         print("Лог версий пуст.")

# # def show_logs(n=None):
# #     """Выводит все логи"""
# #     try:
# #         with open(LOGS_FILE, 'r') as f:
# #             lines = [line.strip() for line in f.readlines() if line.strip()]
# #             if not lines:
# #                 print("Логи пусты.")
# #                 return
# #             if n is not None:
# #                 lines = lines[:n]
# #             for line in lines:
# #                 print(line)
# #     except FileNotFoundError:
# #         print("Логи пусты.")

# # def get_last_log_msg(version_file_path):
# #     """Получает последнее сообщение из лога версий"""
# #     try:
# #         log_dir = os.path.dirname(version_file_path)
# #         log_file = os.path.join(log_dir, 'version_log')
        
# #         if os.path.exists(log_file):
# #             with open(log_file, 'r') as f:
# #                 first_line = f.readline().strip()
# #                 if first_line:
# #                     # Возвращаем часть после последнего ]
# #                     return first_line.split(']')[-1].strip()
# #         return "No version log available"
# #     except Exception as e:
# #         print(f"Error reading log: {str(e)}", file=sys.stderr)
# #         return "Error reading log"

# # def change_path_to_files(absolut_path):
# #     """Изменяет пути к файлам данных"""
# #     global VERSION_FILE, VERSION_LOG_FILE, LOGS_FILE
# #     os.makedirs(absolut_path, exist_ok=True)
# #     VERSION_FILE = os.path.join(absolut_path, 'version')
# #     VERSION_LOG_FILE = os.path.join(absolut_path, 'version_log')
# #     LOGS_FILE = os.path.join(absolut_path, 'logs')

# # def main():
# #     if len(sys.argv) < 3:
# #         print("Ошибка: Недостаточно аргументов. Используйте 'help' для справки.")
# #         sys.exit(1)
    
# #     path = sys.argv[1]
# #     command = sys.argv[2]
    
# #     # Инициализация путей к файлам
# #     change_path_to_files(os.path.dirname(path))
    
# #     # Специальная команда для получения последнего сообщения лога
# #     if command == "get_last_log_msg":
# #         print(get_last_log_msg(path))
# #         return
    
# #     # Логирование вызова команды
# #     timestamp = get_current_timestamp()
# #     log_entry = ' '.join(sys.argv[1:])
    
# #     if command != "log":
# #         prepend_to_file(LOGS_FILE, f'[{timestamp}] {log_entry}')
    
# #     # Обработка команд
# #     if command == 'version':
# #         print_version()
# #     elif command == 'help':
# #         print_help()
# #     elif command in ('patch', 'minor', 'major'):
# #         update_version(command)
# #     elif command == 'drop':
# #         drop_version()
# #     elif command == 'clear':
# #         clear_logs()
# #     elif command == 'undo':
# #         undo_version()
# #     elif command == 'version_log':
# #         n = None
# #         if len(sys.argv) >= 4 and sys.argv[3].startswith('-'):
# #             try:
# #                 n = int(sys.argv[3][1:])
# #             except ValueError:
# #                 print("Ошибка: Неверное число после флага.")
# #                 sys.exit(1)
# #         show_version_log(n)
# #     elif command == 'log':
# #         n = None
# #         if len(sys.argv) >= 4 and sys.argv[3].startswith('-'):
# #             try:
# #                 n = int(sys.argv[3][1:])
# #             except ValueError:
# #                 print("Ошибка: Неверное число после флага.")
# #                 sys.exit(1)
# #         show_logs(n)
# #     else:
# #         print(f"Ошибка: Неизвестная команда '{command}'. Используйте 'help' для справки.")
# #         sys.exit(1)

# # if __name__ == '__main__':
# #     main()
