import xml.etree.ElementTree as ET

def validate_xml(file_path):
    """
    Проверяет XML файл на ошибки и выводит подробную информацию.
    """
    try:
        tree = ET.parse(file_path)
        print("✓ XML файл валиден и успешно распарсен")
        root = tree.getroot()
        print(f"  Корневой элемент: {root.tag}")
        print(f"  Всего элементов: {len(list(root.iter()))}")
        return True
    
    except ET.ParseError as e:
        print(f"❌ Ошибка парсинга XML:")
        print(f"  Строка: {e.position[0]}")
        print(f"  Колонка: {e.position[1]}")
        print(f"  Сообщение: {e.msg}")
        
        # Пытаемся показать контекст ошибки
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                line_num = e.position[0] - 1
                
                if 0 <= line_num < len(lines):
                    print(f"\n  Контекст (строки {max(0, line_num-1)}-{min(len(lines)-1, line_num+2)}):")
                    for i in range(max(0, line_num-1), min(len(lines), line_num+3)):
                        marker = ">>> " if i == line_num else "    "
                        print(f"  {marker}{i+1:4d}: {lines[i].rstrip()}")
        except Exception:
            pass
        
        return False
    
    except FileNotFoundError:
        print(f"❌ Файл не найден: {file_path}")
        return False

if __name__ == "__main__":
    file_path = input("Введите путь к XML файлу: ").strip()
    validate_xml(file_path)
