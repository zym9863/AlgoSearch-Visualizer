"""
核心数据结构模块
实现用于查找算法的基础数据结构类
"""

from typing import List, Optional, Any, Tuple
import random


class SearchableArray:
    """可搜索数组类"""
    
    def __init__(self, data: List[Any] = None):
        self.data = data if data is not None else []
        self.size = len(self.data)
        self.access_history = []  # 记录访问历史
        
    def __len__(self):
        return self.size
    
    def __getitem__(self, index: int):
        """记录访问历史的获取元素方法"""
        if 0 <= index < self.size:
            self.access_history.append(index)
            return self.data[index]
        raise IndexError("数组索引超出范围")
    
    def __setitem__(self, index: int, value: Any):
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError("数组索引超出范围")
    
    def append(self, value: Any):
        """添加元素"""
        self.data.append(value)
        self.size += 1
    
    def clear_history(self):
        """清除访问历史"""
        self.access_history = []
    
    def get_access_history(self):
        """获取访问历史"""
        return self.access_history.copy()
    
    def sort(self):
        """排序数组"""
        self.data.sort()
    
    def generate_random_data(self, size: int, min_val: int = 1, max_val: int = 100):
        """生成随机数据"""
        self.data = [random.randint(min_val, max_val) for _ in range(size)]
        self.size = size
        self.clear_history()


class ListNode:
    """链表节点"""
    
    def __init__(self, val: Any = 0, next_node=None):
        self.val = val
        self.next = next_node


class SearchableLinkedList:
    """可搜索链表类"""
    
    def __init__(self, data: List[Any] = None):
        self.head = None
        self.size = 0
        self.access_history = []  # 记录访问的节点值
        
        if data:
            for value in data:
                self.append(value)
    
    def __len__(self):
        return self.size
    
    def append(self, value: Any):
        """添加元素到链表末尾"""
        new_node = ListNode(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def get_node_at(self, index: int) -> Optional[ListNode]:
        """获取指定索引的节点，记录访问历史"""
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        for i in range(index):
            current = current.next
        
        self.access_history.append(current.val)
        return current
    
    def get_value_at(self, index: int) -> Any:
        """获取指定索引的值"""
        node = self.get_node_at(index)
        return node.val if node else None
    
    def clear_history(self):
        """清除访问历史"""
        self.access_history = []
    
    def get_access_history(self):
        """获取访问历史"""
        return self.access_history.copy()
    
    def to_list(self) -> List[Any]:
        """转换为普通列表"""
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result
    
    def generate_random_data(self, size: int, min_val: int = 1, max_val: int = 100):
        """生成随机数据"""
        self.head = None
        self.size = 0
        self.clear_history()
        
        for _ in range(size):
            value = random.randint(min_val, max_val)
            self.append(value)


class TreeNode:
    """二叉树节点"""
    
    def __init__(self, val: Any = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BinarySearchTree:
    """二叉搜索树类"""
    
    def __init__(self, data: List[Any] = None):
        self.root = None
        self.size = 0
        self.access_history = []  # 记录访问的节点值
        
        if data:
            for value in data:
                self.insert(value)
    
    def __len__(self):
        return self.size
    
    def insert(self, value: Any):
        """插入值"""
        if not self.root:
            self.root = TreeNode(value)
            self.size = 1
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: Any):
        """递归插入"""
        if value < node.val:
            if node.left is None:
                node.left = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.left, value)
        elif value > node.val:
            if node.right is None:
                node.right = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.right, value)
        # 如果值相等，不插入重复值
    
    def search_with_history(self, target: Any) -> Tuple[bool, List[Any]]:
        """搜索值并记录访问路径"""
        self.clear_history()
        found = self._search_recursive(self.root, target)
        return found, self.get_access_history()
    
    def _search_recursive(self, node: Optional[TreeNode], target: Any) -> bool:
        """递归搜索"""
        if node is None:
            return False
        
        self.access_history.append(node.val)
        
        if target == node.val:
            return True
        elif target < node.val:
            return self._search_recursive(node.left, target)
        else:
            return self._search_recursive(node.right, target)
    
    def clear_history(self):
        """清除访问历史"""
        self.access_history = []
    
    def get_access_history(self):
        """获取访问历史"""
        return self.access_history.copy()
    
    def inorder_traversal(self) -> List[Any]:
        """中序遍历"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]):
        """递归中序遍历"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
    
    def get_tree_structure(self) -> List[Tuple[Any, int, str]]:
        """获取树结构用于可视化 (值, 层级, 位置)"""
        if not self.root:
            return []
        
        result = []
        self._get_structure_recursive(self.root, 0, "root", result)
        return result
    
    def _get_structure_recursive(self, node: TreeNode, level: int, position: str, result: List):
        """递归获取树结构"""
        if node:
            result.append((node.val, level, position))
            if node.left:
                self._get_structure_recursive(node.left, level + 1, "left", result)
            if node.right:
                self._get_structure_recursive(node.right, level + 1, "right", result)
    
    def generate_random_data(self, size: int, min_val: int = 1, max_val: int = 100):
        """生成随机数据"""
        self.root = None
        self.size = 0
        self.clear_history()
        
        # 生成不重复的随机数
        values = random.sample(range(min_val, max_val + 1), min(size, max_val - min_val + 1))
        for value in values:
            self.insert(value)


def create_data_structure(ds_type: str, data: List[Any] = None):
    """工厂函数：创建指定类型的数据结构"""
    if ds_type == "array":
        return SearchableArray(data)
    elif ds_type == "linked_list":
        return SearchableLinkedList(data)
    elif ds_type == "binary_search_tree":
        return BinarySearchTree(data)
    else:
        raise ValueError(f"不支持的数据结构类型: {ds_type}")
