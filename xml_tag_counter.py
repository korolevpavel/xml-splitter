import xml.etree.ElementTree as ET
from collections import defaultdict

def count_tags_in_xml(xml_file_path, tag_name):
    """
    Анализирует XML файл и подсчитывает количество тегов с заданным именем.
    
    Args:
        xml_file_path (str): Путь к XML файлу
        tag_name (str): Имя тега для подсчета (например, 'Event' или '{http://v8.1c.ru/8.1/events}Event')
    
    Returns:
        dict: Словарь с результатами анализа
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Подсчет всех элементов с заданным именем
        count = 0
        for element in root.iter():
            # Сравниваем полное имя тега (с namespace)
            if element.tag.endswith(tag_name) or element.tag == tag_name:
                count += 1
        
        return {
            'tag_name': tag_name,
            'total_count': count,
            'status': 'success'
        }
    
    except FileNotFoundError:
        return {
            'status': 'error',
            'message': f'Файл не найден: {xml_file_path}'
        }
    except ET.ParseError as e:
        return {
            'status': 'error',
            'message': f'Ошибка парсинга XML: {str(e)}'
        }

def count_tags_with_namespace(xml_file_path, tag_name, namespace=None):
    """
    Более гибкая версия для работы с namespace.
    
    Args:
        xml_file_path (str): Путь к XML файлу
        tag_name (str): Имя тега (без namespace префикса)
        namespace (str): Namespace URI (опционально), например 'http://v8.1c.ru/8.1/events'
    
    Returns:
        dict: Результаты анализа
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        count = 0
        
        if namespace:
            # Поиск с учетом namespace
            full_tag = f'{{{namespace}}}{tag_name}'
            count = len(root.findall(f'.//{full_tag}'))
        else:
            # Поиск без учета namespace (ищет по локальному имени)
            for element in root.iter():
                local_tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
                if local_tag == tag_name:
                    count += 1
        
        return {
            'tag_name': tag_name,
            'namespace': namespace,
            'total_count': count,
            'status': 'success'
        }
    
    except FileNotFoundError:
        return {
            'status': 'error',
            'message': f'Файл не найден: {xml_file_path}'
        }
    except ET.ParseError as e:
        return {
            'status': 'error',
            'message': f'Ошибка парсинга XML: {str(e)}'
        }

def count_all_tags_by_name(xml_file_path):
    """
    Подсчитывает количество всех уникальных тегов в файле.
    
    Args:
        xml_file_path (str): Путь к XML файлу
    
    Returns:
        dict: Словарь с подсчетом каждого типа тега
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        tag_counts = defaultdict(int)
        
        for element in root.iter():
            # Извлекаем локальное имя тега (без namespace)
            local_tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
            tag_counts[local_tag] += 1
        
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))
    
    except FileNotFoundError:
        return {'error': f'Файл не найден: {xml_file_path}'}
    except ET.ParseError as e:
        return {'error': f'Ошибка парсинга XML: {str(e)}'}


# Примеры использования:
if __name__ == "__main__":
    # Пример 1: Подсчет конкретного тега в файле 1Cv8.xml
    result = count_tags_with_namespace('/1Cv8.xml', 'Event')
    print(f"Количество тегов 'Event': {result['total_count']}")
    
