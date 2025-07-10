"""
算法测试模块
验证查找算法的正确性
"""

import unittest
import random
from data_structures import SearchableArray, SearchableLinkedList, BinarySearchTree
from search_algorithms import SearchAlgorithmFactory


class TestSearchAlgorithms(unittest.TestCase):
    """查找算法测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        self.sorted_data = sorted(self.test_data)
    
    def test_linear_search_array_found(self):
        """测试线性查找 - 数组 - 找到目标"""
        arr = SearchableArray(self.test_data)
        result = SearchAlgorithmFactory.search("linear", arr, 7)
        
        self.assertTrue(result.found)
        self.assertEqual(result.index, 3)  # 7在索引3位置
        self.assertGreater(result.comparisons, 0)
    
    def test_linear_search_array_not_found(self):
        """测试线性查找 - 数组 - 未找到目标"""
        arr = SearchableArray(self.test_data)
        result = SearchAlgorithmFactory.search("linear", arr, 8)
        
        self.assertFalse(result.found)
        self.assertIsNone(result.index)
        self.assertEqual(result.comparisons, len(self.test_data))
    
    def test_linear_search_linked_list_found(self):
        """测试线性查找 - 链表 - 找到目标"""
        linked_list = SearchableLinkedList(self.test_data)
        result = SearchAlgorithmFactory.search("linear", linked_list, 11)
        
        self.assertTrue(result.found)
        self.assertEqual(result.index, 5)  # 11在索引5位置
        self.assertGreater(result.comparisons, 0)
    
    def test_linear_search_linked_list_not_found(self):
        """测试线性查找 - 链表 - 未找到目标"""
        linked_list = SearchableLinkedList(self.test_data)
        result = SearchAlgorithmFactory.search("linear", linked_list, 20)
        
        self.assertFalse(result.found)
        self.assertIsNone(result.index)
        self.assertEqual(result.comparisons, len(self.test_data))
    
    def test_binary_search_found(self):
        """测试二分查找 - 找到目标"""
        arr = SearchableArray(self.sorted_data)
        result = SearchAlgorithmFactory.search("binary", arr, 9)
        
        self.assertTrue(result.found)
        self.assertIsNotNone(result.index)
        self.assertLessEqual(result.comparisons, len(self.sorted_data))
    
    def test_binary_search_not_found(self):
        """测试二分查找 - 未找到目标"""
        arr = SearchableArray(self.sorted_data)
        result = SearchAlgorithmFactory.search("binary", arr, 8)
        
        self.assertFalse(result.found)
        self.assertIsNone(result.index)
        self.assertLessEqual(result.comparisons, len(self.sorted_data))
    
    def test_bst_search_found(self):
        """测试二叉搜索树查找 - 找到目标"""
        bst = BinarySearchTree(self.test_data)
        result = SearchAlgorithmFactory.search("bst", bst, 13)
        
        self.assertTrue(result.found)
        self.assertGreater(result.comparisons, 0)
    
    def test_bst_search_not_found(self):
        """测试二叉搜索树查找 - 未找到目标"""
        bst = BinarySearchTree(self.test_data)
        result = SearchAlgorithmFactory.search("bst", bst, 20)
        
        self.assertFalse(result.found)
        self.assertGreater(result.comparisons, 0)
    
    def test_empty_data_structures(self):
        """测试空数据结构"""
        # 空数组
        empty_arr = SearchableArray([])
        result = SearchAlgorithmFactory.search("linear", empty_arr, 5)
        self.assertFalse(result.found)
        self.assertEqual(result.comparisons, 0)
        
        # 空链表
        empty_list = SearchableLinkedList([])
        result = SearchAlgorithmFactory.search("linear", empty_list, 5)
        self.assertFalse(result.found)
        self.assertEqual(result.comparisons, 0)
        
        # 空二叉搜索树
        empty_bst = BinarySearchTree([])
        result = SearchAlgorithmFactory.search("bst", empty_bst, 5)
        self.assertFalse(result.found)
        self.assertEqual(result.comparisons, 0)
    
    def test_single_element(self):
        """测试单元素数据结构"""
        single_data = [42]
        
        # 单元素数组 - 找到
        arr = SearchableArray(single_data)
        result = SearchAlgorithmFactory.search("linear", arr, 42)
        self.assertTrue(result.found)
        self.assertEqual(result.index, 0)
        self.assertEqual(result.comparisons, 1)
        
        # 单元素数组 - 未找到
        result = SearchAlgorithmFactory.search("linear", arr, 43)
        self.assertFalse(result.found)
        self.assertEqual(result.comparisons, 1)
        
        # 单元素二分查找
        result = SearchAlgorithmFactory.search("binary", arr, 42)
        self.assertTrue(result.found)
        self.assertEqual(result.index, 0)
        self.assertEqual(result.comparisons, 1)
    
    def test_random_data(self):
        """测试随机数据"""
        for _ in range(10):  # 运行10次随机测试
            # 生成随机数据
            size = random.randint(10, 100)
            data = [random.randint(1, 1000) for _ in range(size)]
            sorted_data = sorted(data)
            
            # 选择一个存在的目标值
            target = random.choice(data)
            
            # 测试线性查找
            arr = SearchableArray(data)
            result = SearchAlgorithmFactory.search("linear", arr, target)
            self.assertTrue(result.found)
            
            # 测试二分查找
            sorted_arr = SearchableArray(sorted_data)
            result = SearchAlgorithmFactory.search("binary", sorted_arr, target)
            self.assertTrue(result.found)
            
            # 测试BST查找
            bst = BinarySearchTree(data)
            result = SearchAlgorithmFactory.search("bst", bst, target)
            self.assertTrue(result.found)


class TestDataStructures(unittest.TestCase):
    """数据结构测试类"""
    
    def test_searchable_array(self):
        """测试可搜索数组"""
        data = [1, 2, 3, 4, 5]
        arr = SearchableArray(data)
        
        self.assertEqual(len(arr), 5)
        self.assertEqual(arr[2], 3)
        
        # 测试访问历史
        arr.clear_history()
        _ = arr[0]
        _ = arr[2]
        _ = arr[4]
        history = arr.get_access_history()
        self.assertEqual(history, [0, 2, 4])
    
    def test_searchable_linked_list(self):
        """测试可搜索链表"""
        data = [1, 2, 3, 4, 5]
        linked_list = SearchableLinkedList(data)
        
        self.assertEqual(len(linked_list), 5)
        self.assertEqual(linked_list.get_value_at(2), 3)
        self.assertEqual(linked_list.to_list(), data)
        
        # 测试访问历史
        linked_list.clear_history()
        linked_list.get_value_at(0)
        linked_list.get_value_at(2)
        history = linked_list.get_access_history()
        self.assertEqual(history, [1, 3])
    
    def test_binary_search_tree(self):
        """测试二叉搜索树"""
        data = [5, 3, 7, 1, 9, 4, 6]
        bst = BinarySearchTree(data)
        
        self.assertEqual(len(bst), 7)
        
        # 测试中序遍历（应该是排序的）
        inorder = bst.inorder_traversal()
        self.assertEqual(inorder, sorted(data))
        
        # 测试查找
        found, history = bst.search_with_history(4)
        self.assertTrue(found)
        self.assertIn(4, history)


def run_basic_tests():
    """运行基础测试"""
    print("开始运行基础功能测试...")
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTest(TestSearchAlgorithms('test_linear_search_array_found'))
    suite.addTest(TestSearchAlgorithms('test_binary_search_found'))
    suite.addTest(TestSearchAlgorithms('test_bst_search_found'))
    suite.addTest(TestDataStructures('test_searchable_array'))
    suite.addTest(TestDataStructures('test_binary_search_tree'))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("✅ 所有基础测试通过！")
        return True
    else:
        print("❌ 部分测试失败")
        return False


if __name__ == "__main__":
    # 运行所有测试
    unittest.main(verbosity=2)
