import xml.etree.ElementTree as ET
import os
import sys
from math import ceil

def split_xml_by_tag_count(source_file, tag_name, tags_per_file, output_dir=None, namespace=None):
    """
    Разделяет XML файл на несколько файлов по заданному количеству тегов.
    
    Args:
        source_file (str): Путь к исходному XML файлу
        tag_name (str): Имя тега, который нужно разделить (например, 'Event')
        tags_per_file (int): Количество тегов в каждом файле
        output_dir (str): Директория для сохранения файлов (по умолчанию текущая папка)
        namespace (str): Namespace URI (опционально)
    
    Returns:
        dict: Результаты операции
    """
    try:
        # Парсим исходный файл
        tree = ET.parse(source_file)
        root = tree.getroot()
        
        # Если output_dir не указана, используем текущую директорию
        if output_dir is None:
            output_dir = os.path.dirname(source_file) or '.'
        
        # Создаем директорию, если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Получаем базовое имя файла без расширения
        base_name = os.path.splitext(os.path.basename(source_file))[0]
        
        # Находим все элементы с заданным тегом
        target_elements = []
        
        if namespace:
            full_tag = f'{{{namespace}}}{tag_name}'
            target_elements = root.findall(f'.//{full_tag}')
        else:
            for element in root.iter():
                local_tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
                if local_tag == tag_name:
                    target_elements.append(element)
        
        if not target_elements:
            return {
                'status': 'error',
                'message': f'Теги "{tag_name}" не найдены в файле'
            }
        
        total_elements = len(target_elements)
        num_files = ceil(total_elements / tags_per_file)
        
        created_files = []
        
        # Разделяем элементы на части и создаем новые файлы
        for file_index in range(num_files):
            # Создаем новый корневой элемент с тем же тегом и атрибутами
            new_root = ET.Element(root.tag, root.attrib)
            
            # Копируем все namespace атрибуты
            for key, value in root.attrib.items():
                new_root.set(key, value)
            
            # Определяем диапазон элементов для этого файла
            start_idx = file_index * tags_per_file
            end_idx = min((file_index + 1) * tags_per_file, total_elements)
            
            # Добавляем элементы в новый корень
            for element in target_elements[start_idx:end_idx]:
                # Создаем глубокую копию элемента
                new_root.append(element)
            
            # Формируем имя выходного файла
            output_file = os.path.join(
                output_dir,
                f'{base_name}_part_{file_index + 1:03d}.xml'
            )
            
            # Записываем файл
            tree_new = ET.ElementTree(new_root)
            ET.indent(tree_new, space='    ')  # Красивое форматирование (Python 3.9+)
            tree_new.write(
                output_file,
                encoding='utf-8',
                xml_declaration=True
            )
            
            created_files.append({
                'filename': os.path.basename(output_file),
                'path': output_file,
                'tag_count': end_idx - start_idx
            })
            
            print(f'✓ Создан файл {file_index + 1}/{num_files}: {os.path.basename(output_file)} ({end_idx - start_idx} тегов)')
        
        return {
            'status': 'success',
            'total_elements': total_elements,
            'tags_per_file': tags_per_file,
            'num_files_created': num_files,
            'output_directory': output_dir,
            'created_files': created_files
        }
    
    except FileNotFoundError:
        return {
            'status': 'error',
            'message': f'Файл не найден: {source_file}'
        }
    except ET.ParseError as e:
        return {
            'status': 'error',
            'message': f'Ошибка парсинга XML: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Неожиданная ошибка: {str(e)}'
        }

def main():
    """
    Интерфейс командной строки для разделения XML файлов.
    """
    print("=" * 60)
    print("XML Файл Разделитель")
    print("=" * 60)
    
    # Запрос исходного файла
    source_file = input("\nВведите путь к исходному XML файлу: ").strip()
    
    if not os.path.exists(source_file):
        print(f"❌ Ошибка: файл '{source_file}' не найден")
        return
    
    # Запрос имени тега
    tag_name = input("Введите имя тега для разделения (например, Event): ").strip()
    
    # Запрос количества тегов на файл
    while True:
        try:
            tags_per_file = int(input("Введите количество тегов в каждом файле: ").strip())
            if tags_per_file <= 0:
                print("❌ Количество должно быть положительным числом")
                continue
            break
        except ValueError:
            print("❌ Ошибка: введите корректное число")
    
    # Опциональный запрос директории для сохранения
    output_dir = input("Введите директорию для сохранения файлов (Enter для текущей папки): ").strip()
    if not output_dir:
        output_dir = None
    
    # Запуск разделения
    print("\n⏳ Обработка файла...")
    result = split_xml_by_tag_count(source_file, tag_name, tags_per_file, output_dir)
    
    # Вывод результатов
    print("\n" + "=" * 60)
    if result['status'] == 'success':
        print("✓ УСПЕШНО")
        print(f"  Всего тегов: {result['total_elements']}")
        print(f"  Тегов на файл: {result['tags_per_file']}")
        print(f"  Создано файлов: {result['num_files_created']}")
        print(f"  Папка сохранения: {result['output_directory']}")
        print("\nСозданные файлы:")
        for file_info in result['created_files']:
            print(f"  - {file_info['filename']} ({file_info['tag_count']} тегов)")
    else:
        print(f"❌ ОШИБКА: {result['message']}")
    print("=" * 60)

if __name__ == "__main__":
    # Если аргументы переданы через командную строку, используем их
    if len(sys.argv) == 4:
        source_file = sys.argv[1]
        tag_name = sys.argv[2]
        tags_per_file = int(sys.argv[3])
        
        print(f"Исходный файл: {source_file}")
        print(f"Тег для разделения: {tag_name}")
        print(f"Тегов на файл: {tags_per_file}")
        print()
        
        result = split_xml_by_tag_count(source_file, tag_name, tags_per_file)
        
        if result['status'] == 'success':
            print(f"✓ Успешно создано {result['num_files_created']} файлов")
            for file_info in result['created_files']:
                print(f"  - {file_info['filename']}")
        else:
            print(f"❌ Ошибка: {result['message']}")
    else:
        # Запуск интерактивного режима
        main()
