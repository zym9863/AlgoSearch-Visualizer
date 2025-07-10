"""
查找算法核心实现模块
实现各种查找算法并支持步骤记录功能
"""

from typing import List, Any, Tuple, Dict, Optional
import time
from data_structures import SearchableArray, SearchableLinkedList, BinarySearchTree


class SearchStep:
    """查找步骤记录类"""
    
    def __init__(self, step_num: int, action: str, index: int = None, 
                 value: Any = None, comparison: str = None, found: bool = False):
        self.step_num = step_num
        self.action = action  # "compare", "found", "not_found", "move"
        self.index = index
        self.value = value
        self.comparison = comparison  # "equal", "less", "greater"
        self.found = found
        self.timestamp = time.time()


class SearchResult:
    """查找结果类"""
    
    def __init__(self, found: bool, index: int = None, steps: List[SearchStep] = None,
                 comparisons: int = 0, time_taken: float = 0.0):
        self.found = found
        self.index = index
        self.steps = steps if steps is not None else []
        self.comparisons = comparisons
        self.time_taken = time_taken


class LinearSearch:
    """线性查找算法"""
    
    @staticmethod
    def search(data_structure, target: Any) -> SearchResult:
        """在数据结构中线性查找目标值"""
        start_time = time.time()
        steps = []
        comparisons = 0
        
        if isinstance(data_structure, SearchableArray):
            return LinearSearch._search_array(data_structure, target, steps, start_time)
        elif isinstance(data_structure, SearchableLinkedList):
            return LinearSearch._search_linked_list(data_structure, target, steps, start_time)
        else:
            raise ValueError("线性查找不支持此数据结构类型")
    
    @staticmethod
    def _search_array(arr: SearchableArray, target: Any, steps: List[SearchStep], start_time: float) -> SearchResult:
        """在数组中线性查找"""
        arr.clear_history()
        comparisons = 0
        
        for i in range(len(arr)):
            value = arr[i]  # 这会记录到访问历史中
            comparisons += 1
            
            # 记录比较步骤
            if value == target:
                comparison = "equal"
                found = True
            elif value < target:
                comparison = "less"
                found = False
            else:
                comparison = "greater"
                found = False
            
            step = SearchStep(
                step_num=len(steps) + 1,
                action="compare",
                index=i,
                value=value,
                comparison=comparison,
                found=found
            )
            steps.append(step)
            
            if found:
                end_time = time.time()
                return SearchResult(
                    found=True,
                    index=i,
                    steps=steps,
                    comparisons=comparisons,
                    time_taken=end_time - start_time
                )
        
        # 未找到
        end_time = time.time()
        steps.append(SearchStep(
            step_num=len(steps) + 1,
            action="not_found"
        ))
        
        return SearchResult(
            found=False,
            steps=steps,
            comparisons=comparisons,
            time_taken=end_time - start_time
        )
    
    @staticmethod
    def _search_linked_list(linked_list: SearchableLinkedList, target: Any, 
                          steps: List[SearchStep], start_time: float) -> SearchResult:
        """在链表中线性查找"""
        linked_list.clear_history()
        comparisons = 0
        
        for i in range(len(linked_list)):
            value = linked_list.get_value_at(i)  # 这会记录到访问历史中
            comparisons += 1
            
            # 记录比较步骤
            if value == target:
                comparison = "equal"
                found = True
            elif value < target:
                comparison = "less"
                found = False
            else:
                comparison = "greater"
                found = False
            
            step = SearchStep(
                step_num=len(steps) + 1,
                action="compare",
                index=i,
                value=value,
                comparison=comparison,
                found=found
            )
            steps.append(step)
            
            if found:
                end_time = time.time()
                return SearchResult(
                    found=True,
                    index=i,
                    steps=steps,
                    comparisons=comparisons,
                    time_taken=end_time - start_time
                )
        
        # 未找到
        end_time = time.time()
        steps.append(SearchStep(
            step_num=len(steps) + 1,
            action="not_found"
        ))
        
        return SearchResult(
            found=False,
            steps=steps,
            comparisons=comparisons,
            time_taken=end_time - start_time
        )


class BinarySearch:
    """二分查找算法"""
    
    @staticmethod
    def search(data_structure, target: Any) -> SearchResult:
        """在已排序的数据结构中二分查找目标值"""
        if not isinstance(data_structure, SearchableArray):
            raise ValueError("二分查找只支持数组类型")
        
        start_time = time.time()
        steps = []
        comparisons = 0
        
        data_structure.clear_history()
        left, right = 0, len(data_structure) - 1
        
        while left <= right:
            mid = (left + right) // 2
            value = data_structure[mid]  # 记录访问
            comparisons += 1
            
            # 记录比较步骤
            if value == target:
                comparison = "equal"
                found = True
            elif value < target:
                comparison = "less"
                found = False
            else:
                comparison = "greater"
                found = False
            
            step = SearchStep(
                step_num=len(steps) + 1,
                action="compare",
                index=mid,
                value=value,
                comparison=comparison,
                found=found
            )
            steps.append(step)
            
            if found:
                end_time = time.time()
                return SearchResult(
                    found=True,
                    index=mid,
                    steps=steps,
                    comparisons=comparisons,
                    time_taken=end_time - start_time
                )
            elif value < target:
                left = mid + 1
                steps.append(SearchStep(
                    step_num=len(steps) + 1,
                    action="move",
                    comparison="move_right"
                ))
            else:
                right = mid - 1
                steps.append(SearchStep(
                    step_num=len(steps) + 1,
                    action="move",
                    comparison="move_left"
                ))
        
        # 未找到
        end_time = time.time()
        steps.append(SearchStep(
            step_num=len(steps) + 1,
            action="not_found"
        ))
        
        return SearchResult(
            found=False,
            steps=steps,
            comparisons=comparisons,
            time_taken=end_time - start_time
        )


class BSTSearch:
    """二叉搜索树查找算法"""
    
    @staticmethod
    def search(data_structure, target: Any) -> SearchResult:
        """在二叉搜索树中查找目标值"""
        if not isinstance(data_structure, BinarySearchTree):
            raise ValueError("BST查找只支持二叉搜索树类型")
        
        start_time = time.time()
        found, access_history = data_structure.search_with_history(target)
        end_time = time.time()
        
        steps = []
        comparisons = len(access_history)
        
        # 根据访问历史构建步骤
        for i, value in enumerate(access_history):
            if value == target:
                comparison = "equal"
                step_found = True
            elif value > target:
                comparison = "greater"
                step_found = False
            else:
                comparison = "less"
                step_found = False
            
            step = SearchStep(
                step_num=i + 1,
                action="compare",
                value=value,
                comparison=comparison,
                found=step_found
            )
            steps.append(step)
            
            if step_found:
                break
        
        if not found:
            steps.append(SearchStep(
                step_num=len(steps) + 1,
                action="not_found"
            ))
        
        return SearchResult(
            found=found,
            steps=steps,
            comparisons=comparisons,
            time_taken=end_time - start_time
        )


class SearchAlgorithmFactory:
    """查找算法工厂类"""
    
    algorithms = {
        "linear": LinearSearch,
        "binary": BinarySearch,
        "bst": BSTSearch
    }
    
    @classmethod
    def get_algorithm(cls, algorithm_name: str):
        """获取指定的查找算法"""
        if algorithm_name not in cls.algorithms:
            raise ValueError(f"不支持的算法: {algorithm_name}")
        return cls.algorithms[algorithm_name]
    
    @classmethod
    def get_available_algorithms(cls) -> List[str]:
        """获取所有可用的算法名称"""
        return list(cls.algorithms.keys())
    
    @classmethod
    def search(cls, algorithm_name: str, data_structure, target: Any) -> SearchResult:
        """使用指定算法进行查找"""
        algorithm = cls.get_algorithm(algorithm_name)
        return algorithm.search(data_structure, target)
