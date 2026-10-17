import argparse
from pathlib import Path
import shutil
import sys

def parse_arguments():
    """Парсинг аргументів командного рядка."""
    parser = argparse.ArgumentParser(description="Рекурсивне сортування файлів за розширенням.")
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument(
        "destination", 
        type=Path, 
        nargs="?", 
        default=Path("dist"), 
        help="Шлях до директорії призначення (за замовчуванням: dist)"
    )
    return parser.parse_args()

def copy_file(file_path: Path, dest_root: Path):
    """Копіює файл у відповідну піддиректорію за розширенням."""
    try:
        # Отримуємо розширення файлу без крапки (наприклад, '.txt' -> 'txt')
        extension = file_path.suffix.lstrip('.')
        if not extension:
            extension = "no_extension" # Для файлів без розширення

        # Створюємо шлях до цільової піддиректорії
        target_dir = dest_root / extension
        target_dir.mkdir(parents=True, exist_ok=True)

        # Шлях для нового файлу (зберігаємо оригінальне ім'я)
        target_file = target_dir / file_path.name
        
        # Обробка колізій імен (якщо файл з таким ім'ям вже існує)
        if target_file.exists():
            base_name = file_path.stem
            counter = 1
            while target_file.exists():
                target_file = target_dir / f"{base_name}_{counter}.{extension}"
                counter += 1

        shutil.copy(file_path, target_file)
        print(f"Скопійовано: {file_path} -> {target_file}")
        
    except PermissionError:
        print(f"Помилка доступу до файлу: {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"Непередбачувана помилка при копіюванні {file_path}: {e}", file=sys.stderr)

def recursive_read(current_dir: Path, dest_root: Path):
    """Рекурсивно читає директорію та обробляє її вміст."""
    try:
        for item in current_dir.iterdir():
            if item.is_dir():
                # Рекурсивний виклик для піддиректорії
                recursive_read(item, dest_root)
            elif item.is_file():
                # Обробка файлу
                copy_file(item, dest_root)
                
    except PermissionError:
        print(f"Помилка доступу до директорії: {current_dir}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Директорію не знайдено: {current_dir}", file=sys.stderr)
    except Exception as e:
        print(f"Помилка під час обробки директорії {current_dir}: {e}", file=sys.stderr)

def main():
    args = parse_arguments()
    
    source_dir = args.source
    dest_dir = args.destination

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Помилка: Вихідна директорія '{source_dir}' не існує або не є папкою.", file=sys.stderr)
        sys.exit(1)

    print(f"Початок сортування з '{source_dir}' у '{dest_dir}'...")
    recursive_read(source_dir, dest_dir)
    print("Сортування успішно завершено!")

if __name__ == "__main__":
    main()