"""
性能测试模块
实现性能基准测试功能，包括时间测量、比较次数统计、批量测试和结果对比分析
"""

import time
import random
import statistics
from typing import List, Dict, Any, Tuple
import pandas as pd
from data_structures import create_data_structure
from search_algorithms import SearchAlgorithmFactory, SearchResult


class PerformanceMetrics:
    """性能指标类"""
    
    def __init__(self):
        self.algorithm_name = ""
        self.data_structure_type = ""
        self.data_size = 0
        self.search_times = []  # 查找时间列表
        self.comparison_counts = []  # 比较次数列表
        self.success_rate = 0.0  # 成功率
        self.total_tests = 0
        self.successful_searches = 0
    
    def add_result(self, result: SearchResult):
        """添加一个查找结果"""
        self.search_times.append(result.time_taken)
        self.comparison_counts.append(result.comparisons)
        self.total_tests += 1
        if result.found:
            self.successful_searches += 1
    
    def calculate_statistics(self):
        """计算统计指标"""
        if not self.search_times:
            return
        
        self.success_rate = self.successful_searches / self.total_tests if self.total_tests > 0 else 0
        
        # 时间统计
        self.avg_time = statistics.mean(self.search_times)
        self.min_time = min(self.search_times)
        self.max_time = max(self.search_times)
        self.median_time = statistics.median(self.search_times)
        
        # 比较次数统计
        self.avg_comparisons = statistics.mean(self.comparison_counts)
        self.min_comparisons = min(self.comparison_counts)
        self.max_comparisons = max(self.comparison_counts)
        self.median_comparisons = statistics.median(self.comparison_counts)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        self.calculate_statistics()
        return {
            "算法名称": self.algorithm_name,
            "数据结构": self.data_structure_type,
            "数据规模": self.data_size,
            "测试次数": self.total_tests,
            "成功率": f"{self.success_rate:.2%}",
            "平均时间(ms)": f"{self.avg_time * 1000:.4f}",
            "最小时间(ms)": f"{self.min_time * 1000:.4f}",
            "最大时间(ms)": f"{self.max_time * 1000:.4f}",
            "中位时间(ms)": f"{self.median_time * 1000:.4f}",
            "平均比较次数": f"{self.avg_comparisons:.2f}",
            "最小比较次数": self.min_comparisons,
            "最大比较次数": self.max_comparisons,
            "中位比较次数": f"{self.median_comparisons:.2f}"
        }


class PerformanceTester:
    """性能测试器"""
    
    def __init__(self):
        self.results = {}  # 存储测试结果
    
    def single_algorithm_test(self, algorithm_name: str, data_structure_type: str,
                            data_size: int, test_count: int = 100,
                            target_ratio: float = 0.5) -> PerformanceMetrics:
        """单个算法性能测试"""
        metrics = PerformanceMetrics()
        metrics.algorithm_name = algorithm_name
        metrics.data_structure_type = data_structure_type
        metrics.data_size = data_size
        
        for _ in range(test_count):
            # 创建数据结构并生成随机数据
            data_structure = create_data_structure(data_structure_type)
            data_structure.generate_random_data(data_size)
            
            # 对于二分查找，需要排序
            if algorithm_name == "binary" and hasattr(data_structure, 'sort'):
                data_structure.sort()
            
            # 选择目标值（一定比例存在于数据中）
            if random.random() < target_ratio:
                # 选择存在的值
                if data_structure_type == "array":
                    target = random.choice(data_structure.data)
                elif data_structure_type == "linked_list":
                    target = random.choice(data_structure.to_list())
                elif data_structure_type == "binary_search_tree":
                    target = random.choice(data_structure.inorder_traversal())
            else:
                # 选择不存在的值
                target = random.randint(1000, 2000)
            
            # 执行查找
            try:
                result = SearchAlgorithmFactory.search(algorithm_name, data_structure, target)
                metrics.add_result(result)
            except Exception as e:
                print(f"测试出错: {e}")
                continue
        
        return metrics
    
    def batch_test(self, algorithms: List[str], data_structure_types: List[str],
                   data_sizes: List[int], test_count: int = 100) -> Dict[str, PerformanceMetrics]:
        """批量测试多个算法"""
        results = {}
        
        for algorithm in algorithms:
            for ds_type in data_structure_types:
                for size in data_sizes:
                    # 检查算法和数据结构的兼容性
                    if not self._is_compatible(algorithm, ds_type):
                        continue
                    
                    print(f"测试 {algorithm} 算法在 {ds_type} (大小: {size}) 上的性能...")
                    
                    metrics = self.single_algorithm_test(
                        algorithm, ds_type, size, test_count
                    )
                    
                    key = f"{algorithm}_{ds_type}_{size}"
                    results[key] = metrics
        
        self.results = results
        return results
    
    def _is_compatible(self, algorithm: str, data_structure_type: str) -> bool:
        """检查算法和数据结构的兼容性"""
        compatibility = {
            "linear": ["array", "linked_list"],
            "binary": ["array"],
            "bst": ["binary_search_tree"]
        }
        
        return data_structure_type in compatibility.get(algorithm, [])
    
    def generate_comparison_report(self) -> pd.DataFrame:
        """生成对比报告"""
        if not self.results:
            return pd.DataFrame()
        
        report_data = []
        for metrics in self.results.values():
            report_data.append(metrics.to_dict())
        
        return pd.DataFrame(report_data)
    
    def get_best_algorithm_by_metric(self, metric: str = "avg_time") -> Dict[str, Any]:
        """根据指标找出最佳算法"""
        if not self.results:
            return {}
        
        best_results = {}
        
        # 按数据结构和大小分组
        groups = {}
        for key, metrics in self.results.items():
            algorithm, ds_type, size = key.split('_')
            group_key = f"{ds_type}_{size}"
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append((algorithm, metrics))
        
        # 为每组找出最佳算法
        for group_key, algorithms in groups.items():
            if metric == "avg_time":
                best = min(algorithms, key=lambda x: x[1].avg_time)
            elif metric == "avg_comparisons":
                best = min(algorithms, key=lambda x: x[1].avg_comparisons)
            elif metric == "success_rate":
                best = max(algorithms, key=lambda x: x[1].success_rate)
            else:
                continue
            
            best_results[group_key] = {
                "algorithm": best[0],
                "metrics": best[1].to_dict()
            }
        
        return best_results
    
    def complexity_analysis(self, algorithm: str, data_structure_type: str,
                          size_range: List[int], test_count: int = 50) -> pd.DataFrame:
        """复杂度分析"""
        analysis_data = []
        
        for size in size_range:
            print(f"分析 {algorithm} 在大小 {size} 的数据上的复杂度...")
            
            metrics = self.single_algorithm_test(
                algorithm, data_structure_type, size, test_count
            )
            
            analysis_data.append({
                "数据规模": size,
                "平均时间(ms)": metrics.avg_time * 1000,
                "平均比较次数": metrics.avg_comparisons,
                "最大比较次数": metrics.max_comparisons
            })
        
        return pd.DataFrame(analysis_data)


class BenchmarkSuite:
    """基准测试套件"""
    
    def __init__(self):
        self.tester = PerformanceTester()
    
    def run_standard_benchmark(self) -> Dict[str, Any]:
        """运行标准基准测试"""
        print("开始运行标准基准测试...")
        
        # 测试配置
        algorithms = ["linear", "binary", "bst"]
        data_structure_types = ["array", "linked_list", "binary_search_tree"]
        data_sizes = [100, 500, 1000, 2000]
        test_count = 50
        
        # 执行批量测试
        results = self.tester.batch_test(algorithms, data_structure_types, data_sizes, test_count)
        
        # 生成报告
        comparison_report = self.tester.generate_comparison_report()
        best_by_time = self.tester.get_best_algorithm_by_metric("avg_time")
        best_by_comparisons = self.tester.get_best_algorithm_by_metric("avg_comparisons")
        
        return {
            "detailed_results": results,
            "comparison_report": comparison_report,
            "best_by_time": best_by_time,
            "best_by_comparisons": best_by_comparisons
        }
    
    def run_complexity_analysis(self) -> Dict[str, pd.DataFrame]:
        """运行复杂度分析"""
        print("开始运行复杂度分析...")
        
        size_range = [50, 100, 200, 500, 1000, 2000, 5000]
        
        analyses = {}
        
        # 线性查找在数组上
        analyses["linear_array"] = self.tester.complexity_analysis(
            "linear", "array", size_range
        )
        
        # 二分查找在数组上
        analyses["binary_array"] = self.tester.complexity_analysis(
            "binary", "array", size_range
        )
        
        # BST查找
        analyses["bst_tree"] = self.tester.complexity_analysis(
            "bst", "binary_search_tree", size_range
        )
        
        return analyses
