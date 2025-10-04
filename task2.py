"""
Завдання 2: Розширення функціоналу префіксного дерева

Реалізація додаткових методів для класу Trie:
- count_words_with_suffix(pattern) - підрахунок слів, що закінчуються заданим шаблоном
- has_prefix(prefix) - перевірка наявності слів із заданим префіксом
"""

from trie import Trie


class Homework(Trie):
    """Розширений клас Trie з додатковим функціоналом"""
    
    def count_words_with_suffix(self, pattern: str) -> int:
        """
        Підраховує кількість слів, що закінчуються заданим суфіксом
        
        Args:
            pattern: суфікс для пошуку
            
        Returns:
            Кількість слів, що закінчуються на заданий суфікс
            
        Raises:
            TypeError: якщо pattern не є рядком
            ValueError: якщо pattern порожній
        """
        # Валідація вхідних даних
        if not isinstance(pattern, str):
            raise TypeError("Шаблон повинен бути рядком")
        
        if not pattern:
            raise ValueError("Шаблон не може бути порожнім")
        
        # Отримуємо всі ключі з Trie
        all_keys = self.keys()
        
        # Підраховуємо слова, що закінчуються на заданий суфікс
        count = 0
        for key in all_keys:
            if key.endswith(pattern):
                count += 1
        
        return count
    
    def has_prefix(self, prefix: str) -> bool:
        """
        Перевіряє, чи існує хоча б одне слово з заданим префіксом
        
        Args:
            prefix: префікс для перевірки
            
        Returns:
            True, якщо існує слово з таким префіксом, False інакше
            
        Raises:
            TypeError: якщо prefix не є рядком
            ValueError: якщо prefix порожній
        """
        # Валідація вхідних даних
        if not isinstance(prefix, str):
            raise TypeError("Префікс повинен бути рядком")
        
        if not prefix:
            raise ValueError("Префікс не може бути порожнім")
        
        # Ефективна перевірка наявності префікса
        current = self.root
        
        # Проходимо по символах префікса
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        
        # Перевіряємо, чи є хоча б одне слово, що починається з цього префікса
        return self._has_words_in_subtree(current)
    
    def _has_words_in_subtree(self, node) -> bool:
        """
        Допоміжний метод для перевірки наявності слів у піддереві
        
        Args:
            node: вузол Trie для перевірки
            
        Returns:
            True, якщо в піддереві є хоча б одне слово
        """
        # Якщо поточний вузол є кінцем слова
        if node.is_end_of_word:
            return True
        
        # Рекурсивно перевіряємо всі дочірні вузли
        for child in node.children.values():
            if self._has_words_in_subtree(child):
                return True
        
        return False
    
    def get_words_with_suffix(self, pattern: str) -> list:
        """
        Додатковий метод: повертає список слів, що закінчуються заданим суфіксом
        
        Args:
            pattern: суфікс для пошуку
            
        Returns:
            Список слів з заданим суфіксом
        """
        if not isinstance(pattern, str):
            raise TypeError("Шаблон повинен бути рядком")
        
        if not pattern:
            raise ValueError("Шаблон не може бути порожнім")
        
        all_keys = self.keys()
        return [key for key in all_keys if key.endswith(pattern)]
    
    def get_statistics(self) -> dict:
        """
        Додатковий метод: повертає статистику про Trie
        
        Returns:
            Словник зі статистикою
        """
        all_keys = self.keys()
        
        if not all_keys:
            return {
                'total_words': 0,
                'total_characters': 0,
                'average_word_length': 0,
                'shortest_word': None,
                'longest_word': None,
                'unique_prefixes': 0
            }
        
        total_words = len(all_keys)
        total_characters = sum(len(word) for word in all_keys)
        average_length = total_characters / total_words if total_words > 0 else 0
        
        shortest_word = min(all_keys, key=len)
        longest_word = max(all_keys, key=len)
        
        # Підрахунок унікальних префіксів
        prefixes = set()
        for word in all_keys:
            for i in range(1, len(word) + 1):
                prefixes.add(word[:i])
        
        return {
            'total_words': total_words,
            'total_characters': total_characters,
            'average_word_length': round(average_length, 2),
            'shortest_word': shortest_word,
            'longest_word': longest_word,
            'unique_prefixes': len(prefixes)
        }


def run_comprehensive_tests():
    """Комплексне тестування класу Homework"""
    print("=" * 60)
    print("КОМПЛЕКСНЕ ТЕСТУВАННЯ КЛАСУ HOMEWORK")
    print("=" * 60)
    
    # Створюємо екземпляр і додаємо тестові дані
    trie = Homework()
    test_words = ["apple", "application", "banana", "cat", "catastrophe", "car", "card", "care", "careful"]
    
    print("Додавання тестових слів...")
    for i, word in enumerate(test_words):
        trie.put(word, i)
    
    print(f"Додано слова: {test_words}")
    print()
    
    # Тестування count_words_with_suffix
    print("ТЕСТУВАННЯ count_words_with_suffix:")
    print("-" * 40)
    
    test_suffixes = ["e", "ion", "a", "at", "car", "ful", "xyz"]
    for suffix in test_suffixes:
        count = trie.count_words_with_suffix(suffix)
        words = trie.get_words_with_suffix(suffix)
        print(f"Суфікс '{suffix}': {count} слів - {words}")
    
    print()
    
    # Тестування has_prefix
    print("ТЕСТУВАННЯ has_prefix:")
    print("-" * 40)
    
    test_prefixes = ["app", "cat", "car", "ban", "bat", "xyz", "a", "c"]
    for prefix in test_prefixes:
        has_prefix = trie.has_prefix(prefix)
        words_with_prefix = trie.keys_with_prefix(prefix)
        print(f"Префікс '{prefix}': {has_prefix} - {words_with_prefix}")
    
    print()
    
    # Тестування обробки помилок
    print("ТЕСТУВАННЯ ОБРОБКИ ПОМИЛОК:")
    print("-" * 40)
    
    error_tests = [
        (lambda: trie.count_words_with_suffix(123), "count_words_with_suffix з числом"),
        (lambda: trie.count_words_with_suffix(""), "count_words_with_suffix з порожнім рядком"),
        (lambda: trie.has_prefix(None), "has_prefix з None"),
        (lambda: trie.has_prefix(""), "has_prefix з порожнім рядком"),
    ]
    
    for test_func, description in error_tests:
        try:
            test_func()
            print(f"❌ {description}: помилка НЕ викинута")
        except (TypeError, ValueError) as e:
            print(f"✅ {description}: правильно викинута помилка - {type(e).__name__}")
        except Exception as e:
            print(f"⚠️ {description}: неочікувана помилка - {type(e).__name__}")
    
    print()
    
    # Статистика
    print("СТАТИСТИКА TRIE:")
    print("-" * 40)
    stats = trie.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print()
    print("=" * 60)
    print("ТЕСТУВАННЯ ЗАВЕРШЕНО")
    print("=" * 60)


# Основні тести із завдання
if __name__ == "__main__":
    print("Виконання основних тестів із завдання...")
    
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
    
    print("✅ Усі основні тести пройдено успішно!")
    print()
    
    # Запуск комплексного тестування
    run_comprehensive_tests()