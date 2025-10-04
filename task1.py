"""
Завдання 1: Застосування алгоритму максимального потоку для логістики товарів

Реалізація алгоритму Едмондса-Карпа для знаходження максимального потоку 
в мережі логістики товарів від терміналів до магазинів через склади.
"""

from collections import defaultdict, deque
from typing import Dict, List, Tuple, Any


class MaxFlowNetwork:
    """Клас для реалізації алгоритму максимального потоку"""
    
    def __init__(self):
        self.graph = defaultdict(dict)
        self.original_capacities = defaultdict(dict)
        self.vertices = set()
        
    def add_edge(self, from_node: str, to_node: str, capacity: int):
        """Додає ребро до графа з заданою пропускною здатністю"""
        self.graph[from_node][to_node] = capacity
        self.graph[to_node][from_node] = 0  # Зворотне ребро
        self.original_capacities[from_node][to_node] = capacity
        self.vertices.add(from_node)
        self.vertices.add(to_node)
        
    def bfs(self, source: str, sink: str, parent: Dict[str, str]) -> bool:
        """
        Пошук в ширину для знаходження шляху від джерела до стоку
        Повертає True, якщо існує шлях від source до sink
        """
        visited = set()
        queue = deque([source])
        visited.add(source)
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self.graph[current]:
                if neighbor not in visited and self.graph[current][neighbor] > 0:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
                    if neighbor == sink:
                        return True
        return False
    
    def edmonds_karp(self, source: str, sink: str) -> int:
        """
        Алгоритм Едмондса-Карпа для знаходження максимального потоку
        """
        parent = {}
        max_flow = 0
        
        # Поки існує шлях від джерела до стоку
        while self.bfs(source, sink, parent):
            # Знаходимо мінімальну пропускну здатність на шляху
            path_flow = float('Inf')
            s = sink
            path = []
            
            # Відновлюємо шлях від стоку до джерела
            while s != source:
                path.append((parent[s], s))
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            
            # Додаємо знайдений потік до загального потоку
            max_flow += path_flow
            
            # Оновлюємо залишкові пропускні здатності
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
                
            parent.clear()
            
        return max_flow
    
    def get_flow_analysis(self) -> Dict[str, Any]:
        """Повертає детальний аналіз потоків у мережі"""
        flows = {}
        terminal_flows = {}
        store_flows = {}
        
        # Аналізуємо потоки між усіма вузлами
        for from_node in self.original_capacities:
            for to_node in self.original_capacities[from_node]:
                original_capacity = self.original_capacities[from_node][to_node]
                remaining_capacity = self.graph[from_node][to_node]
                flow = original_capacity - remaining_capacity
                
                if flow > 0:
                    flows[(from_node, to_node)] = flow
                    
                    # Збираємо потоки від терміналів
                    if from_node.startswith('Термінал'):
                        if from_node not in terminal_flows:
                            terminal_flows[from_node] = 0
                        terminal_flows[from_node] += flow
                    
                    # Збираємо потоки до магазинів
                    if to_node.startswith('Магазин'):
                        if to_node not in store_flows:
                            store_flows[to_node] = 0
                        store_flows[to_node] += flow
        
        return {
            'flows': flows,
            'terminal_flows': terminal_flows,
            'store_flows': store_flows
        }


def create_logistics_network():
    """Створює мережу логістики товарів згідно із завданням"""
    network = MaxFlowNetwork()
    
    # Додаємо віртуальні джерело та стік
    super_source = "Супер-джерело"
    super_sink = "Супер-стік"
    
    # З'єднуємо супер-джерело з терміналами (необмежена пропускна здатність)
    network.add_edge(super_source, "Термінал 1", float('inf'))
    network.add_edge(super_source, "Термінал 2", float('inf'))
    
    # Зв'язки від терміналів до складів
    terminal_warehouse_connections = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
    ]
    
    for from_terminal, to_warehouse, capacity in terminal_warehouse_connections:
        network.add_edge(from_terminal, to_warehouse, capacity)
    
    # Зв'язки від складів до магазинів
    warehouse_store_connections = [
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    
    for from_warehouse, to_store, capacity in warehouse_store_connections:
        network.add_edge(from_warehouse, to_store, capacity)
    
    # З'єднуємо магазини з супер-стоком (необмежена пропускна здатність)
    stores = [f"Магазин {i}" for i in range(1, 15)]
    for store in stores:
        network.add_edge(store, super_sink, float('inf'))
    
    return network, super_source, super_sink


def calculate_terminal_to_store_flow(network: MaxFlowNetwork, terminal: str, store: str, flows: Dict[Tuple[str, str], int]) -> int:
    """Обчислює потік від конкретного терміналу до конкретного магазину"""
    # Простий підхід: якщо потік йде через склад, розподіляємо пропорційно
    total_flow = 0
    
    # Знаходимо всі склади, через які проходить потік від терміналу
    terminal_warehouse_flows = {}
    for (from_node, to_node), flow in flows.items():
        if from_node == terminal and to_node.startswith('Склад'):
            terminal_warehouse_flows[to_node] = flow
    
    # Для кожного складу обчислюємо, скільки йде до нашого магазину
    for warehouse, terminal_to_warehouse_flow in terminal_warehouse_flows.items():
        if (warehouse, store) in flows:
            warehouse_to_store_flow = flows[(warehouse, store)]
            
            # Обчислюємо загальний потік з цього складу
            total_warehouse_output = sum(
                flow for (from_w, to_s), flow in flows.items() 
                if from_w == warehouse and to_s.startswith('Магазин')
            )
            
            if total_warehouse_output > 0:
                # Пропорційно розподіляємо потік від терміналу
                proportion = warehouse_to_store_flow / total_warehouse_output
                total_flow += int(terminal_to_warehouse_flow * proportion)
    
    return total_flow


def find_bottleneck_routes(network: MaxFlowNetwork) -> List[Tuple[Tuple[str, str], int]]:
    """Знаходить маршрути з найменшою пропускною здатністю"""
    bottlenecks = []
    min_capacity = float('inf')
    
    for from_node in network.original_capacities:
        for to_node in network.original_capacities[from_node]:
            capacity = network.original_capacities[from_node][to_node]
            if capacity < min_capacity and capacity != float('inf'):
                min_capacity = capacity
                bottlenecks = [((from_node, to_node), capacity)]
            elif capacity == min_capacity and capacity != float('inf'):
                bottlenecks.append(((from_node, to_node), capacity))
    
    return bottlenecks


def identify_bottlenecks(network: MaxFlowNetwork, flows: Dict[Tuple[str, str], int]) -> List[str]:
    """Ідентифікує вузькі місця в мережі"""
    bottlenecks = []
    
    # Знаходимо ребра, які використовуються на повну потужність
    for (from_node, to_node), flow in flows.items():
        original_capacity = network.original_capacities[from_node][to_node]
        if flow == original_capacity and original_capacity != float('inf'):
            bottlenecks.append(f"{from_node} → {to_node} (повністю завантажено: {flow}/{original_capacity})")
    
    return bottlenecks


def analyze_results(network: MaxFlowNetwork, max_flow: int):
    """Аналізує результати та створює звіт"""
    analysis = network.get_flow_analysis()
    
    print(f"\n{'='*60}")
    print(f"ЗВІТ ПРО МАКСИМАЛЬНИЙ ПОТІК У ЛОГІСТИЧНІЙ МЕРЕЖІ")
    print(f"{'='*60}")
    print(f"Максимальний потік: {max_flow} одиниць товару")
    print(f"{'='*60}")
    
    # Створюємо таблицю потоків між терміналами та магазинами
    print("\nТАБЛИЦЯ ПОТОКІВ МІЖ ТЕРМІНАЛАМИ ТА МАГАЗИНАМИ:")
    print("-" * 60)
    print(f"{'Термінал':<15} {'Магазин':<15} {'Фактичний Потік (одиниць)':<25}")
    print("-" * 60)
    
    for terminal in ['Термінал 1', 'Термінал 2']:
        for store in [f'Магазин {i}' for i in range(1, 15)]:
            # Обчислюємо потік від терміналу до магазину через склади
            terminal_to_store_flow = calculate_terminal_to_store_flow(
                network, terminal, store, analysis['flows']
            )
            if terminal_to_store_flow > 0:
                print(f"{terminal:<15} {store:<15} {terminal_to_store_flow:<25}")
    
    # Аналіз потоків по терміналах
    print(f"\n\nАНАЛІЗ ПОТОКІВ ПО ТЕРМІНАЛАХ:")
    print("-" * 40)
    for terminal, flow in analysis['terminal_flows'].items():
        print(f"{terminal}: {flow} одиниць")
    
    # Аналіз потоків по магазинах
    print(f"\nАНАЛІЗ ПОСТАЧАННЯ ПО МАГАЗИНАХ:")
    print("-" * 40)
    for store, flow in sorted(analysis['store_flows'].items()):
        print(f"{store}: {flow} одиниць")
    
    # Відповіді на аналітичні питання
    print(f"\n\nВІДПОВІДІ НА АНАЛІТИЧНІ ПИТАННЯ:")
    print("=" * 50)
    
    # 1. Які термінали забезпечують найбільший потік
    max_terminal_flow = max(analysis['terminal_flows'].values())
    top_terminals = [t for t, f in analysis['terminal_flows'].items() if f == max_terminal_flow]
    print(f"1. Термінали з найбільшим потоком ({max_terminal_flow} одиниць): {', '.join(top_terminals)}")
    
    # 2. Маршрути з найменшою пропускною здатністю
    min_capacity_routes = find_bottleneck_routes(network)
    print(f"2. Маршрути з найменшою пропускною здатністю:")
    for route, capacity in min_capacity_routes:
        print(f"   {route[0]} → {route[1]}: {capacity} одиниць")
    
    # 3. Магазини з найменшим постачанням
    min_store_flow = min(analysis['store_flows'].values())
    min_stores = [s for s, f in analysis['store_flows'].items() if f == min_store_flow]
    print(f"3. Магазини з найменшим постачанням ({min_store_flow} одиниць): {', '.join(min_stores)}")
    
    # 4. Вузькі місця
    bottlenecks = identify_bottlenecks(network, analysis['flows'])
    print(f"4. Виявлені вузькі місця:")
    for bottleneck in bottlenecks:
        print(f"   {bottleneck}")


def main():
    """Основна функція програми"""
    print("Створення мережі логістики товарів...")
    network, source, sink = create_logistics_network()
    
    print("Застосування алгоритму Едмондса-Карпа...")
    max_flow = network.edmonds_karp(source, sink)
    
    print("Аналіз результатів...")
    analyze_results(network, max_flow)
    
    return network, max_flow


if __name__ == "__main__":
    network, max_flow = main()