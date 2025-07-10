"""
可视化组件模块
实现数据结构的图形化展示和算法执行过程的动态可视化
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
import time

from data_structures import SearchableArray, SearchableLinkedList, BinarySearchTree
from search_algorithms import SearchStep, SearchResult


class DataStructureVisualizer:
    """数据结构可视化器"""
    
    @staticmethod
    def visualize_array(arr: SearchableArray, highlighted_indices: List[int] = None,
                       target_value: Any = None, title: str = "数组可视化") -> go.Figure:
        """可视化数组"""
        if highlighted_indices is None:
            highlighted_indices = []
        
        # 创建颜色列表
        colors = []
        for i, value in enumerate(arr.data):
            if i in highlighted_indices:
                if value == target_value:
                    colors.append('red')  # 找到目标
                else:
                    colors.append('orange')  # 正在比较
            else:
                colors.append('lightblue')  # 未访问
        
        fig = go.Figure(data=go.Bar(
            x=list(range(len(arr.data))),
            y=arr.data,
            marker_color=colors,
            text=arr.data,
            textposition='auto',
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="索引",
            yaxis_title="值",
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def visualize_linked_list(linked_list: SearchableLinkedList, 
                            highlighted_indices: List[int] = None,
                            target_value: Any = None, 
                            title: str = "链表可视化") -> go.Figure:
        """可视化链表"""
        if highlighted_indices is None:
            highlighted_indices = []
        
        data = linked_list.to_list()
        
        # 创建节点位置
        x_positions = list(range(len(data)))
        y_positions = [0] * len(data)
        
        # 创建颜色列表
        colors = []
        for i, value in enumerate(data):
            if i in highlighted_indices:
                if value == target_value:
                    colors.append('red')  # 找到目标
                else:
                    colors.append('orange')  # 正在比较
            else:
                colors.append('lightblue')  # 未访问
        
        fig = go.Figure()
        
        # 添加节点
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_positions,
            mode='markers+text',
            marker=dict(size=40, color=colors),
            text=data,
            textposition='middle center',
            name='节点'
        ))
        
        # 添加连接线
        for i in range(len(data) - 1):
            fig.add_trace(go.Scatter(
                x=[x_positions[i], x_positions[i + 1]],
                y=[y_positions[i], y_positions[i + 1]],
                mode='lines',
                line=dict(color='gray', width=2),
                showlegend=False
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="位置",
            showlegend=False,
            height=200,
            yaxis=dict(visible=False)
        )
        
        return fig
    
    @staticmethod
    def visualize_binary_tree(bst: BinarySearchTree, highlighted_values: List[Any] = None,
                            target_value: Any = None, title: str = "二叉搜索树可视化") -> go.Figure:
        """可视化二叉搜索树"""
        if highlighted_values is None:
            highlighted_values = []
        
        tree_structure = bst.get_tree_structure()
        if not tree_structure:
            fig = go.Figure()
            fig.update_layout(title="空树")
            return fig
        
        # 计算节点位置
        positions = DataStructureVisualizer._calculate_tree_positions(tree_structure)
        
        fig = go.Figure()
        
        # 添加边
        DataStructureVisualizer._add_tree_edges(fig, bst.root, positions)
        
        # 添加节点
        x_coords = []
        y_coords = []
        node_colors = []
        node_texts = []
        
        for value, level, position in tree_structure:
            x, y = positions[value]
            x_coords.append(x)
            y_coords.append(y)
            node_texts.append(str(value))
            
            if value in highlighted_values:
                if value == target_value:
                    node_colors.append('red')  # 找到目标
                else:
                    node_colors.append('orange')  # 正在比较
            else:
                node_colors.append('lightblue')  # 未访问
        
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            marker=dict(size=30, color=node_colors),
            text=node_texts,
            textposition='middle center',
            name='节点'
        ))
        
        fig.update_layout(
            title=title,
            showlegend=False,
            height=500,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig
    
    @staticmethod
    def _calculate_tree_positions(tree_structure: List[Tuple]) -> Dict[Any, Tuple[float, float]]:
        """计算树节点位置"""
        positions = {}
        level_counts = {}
        level_indices = {}
        
        # 统计每层的节点数
        for value, level, position in tree_structure:
            if level not in level_counts:
                level_counts[level] = 0
                level_indices[level] = 0
            level_counts[level] += 1
        
        # 计算位置
        for value, level, position in tree_structure:
            max_width = max(level_counts.values()) if level_counts else 1
            level_width = level_counts[level]
            
            # 水平位置
            if level_width == 1:
                x = 0
            else:
                spacing = max_width / level_width
                x = (level_indices[level] - (level_width - 1) / 2) * spacing
            
            # 垂直位置
            y = -level
            
            positions[value] = (x, y)
            level_indices[level] += 1
        
        return positions
    
    @staticmethod
    def _add_tree_edges(fig: go.Figure, node, positions: Dict[Any, Tuple[float, float]]):
        """添加树的边"""
        if node is None:
            return
        
        if node.left:
            x1, y1 = positions[node.val]
            x2, y2 = positions[node.left.val]
            fig.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode='lines',
                line=dict(color='gray', width=2),
                showlegend=False
            ))
            DataStructureVisualizer._add_tree_edges(fig, node.left, positions)
        
        if node.right:
            x1, y1 = positions[node.val]
            x2, y2 = positions[node.right.val]
            fig.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode='lines',
                line=dict(color='gray', width=2),
                showlegend=False
            ))
            DataStructureVisualizer._add_tree_edges(fig, node.right, positions)


class SearchVisualizationController:
    """查找可视化控制器"""
    
    def __init__(self):
        self.current_step = 0
        self.search_result = None
        self.data_structure = None
        self.target_value = None
    
    def setup_search(self, data_structure, target_value: Any, search_result: SearchResult):
        """设置查找可视化"""
        self.data_structure = data_structure
        self.target_value = target_value
        self.search_result = search_result
        self.current_step = 0
    
    def get_current_visualization(self) -> go.Figure:
        """获取当前步骤的可视化"""
        if not self.search_result or not self.data_structure:
            return go.Figure()
        
        # 获取当前步骤需要高亮的元素
        highlighted_elements = self._get_highlighted_elements()
        
        # 根据数据结构类型生成可视化
        if isinstance(self.data_structure, SearchableArray):
            return DataStructureVisualizer.visualize_array(
                self.data_structure, 
                highlighted_elements, 
                self.target_value,
                f"步骤 {self.current_step + 1}: 数组查找"
            )
        elif isinstance(self.data_structure, SearchableLinkedList):
            return DataStructureVisualizer.visualize_linked_list(
                self.data_structure, 
                highlighted_elements, 
                self.target_value,
                f"步骤 {self.current_step + 1}: 链表查找"
            )
        elif isinstance(self.data_structure, BinarySearchTree):
            highlighted_values = []
            if self.current_step < len(self.search_result.steps):
                for i in range(self.current_step + 1):
                    step = self.search_result.steps[i]
                    if step.value is not None:
                        highlighted_values.append(step.value)
            
            return DataStructureVisualizer.visualize_binary_tree(
                self.data_structure, 
                highlighted_values, 
                self.target_value,
                f"步骤 {self.current_step + 1}: 二叉搜索树查找"
            )
        
        return go.Figure()
    
    def _get_highlighted_elements(self) -> List[int]:
        """获取需要高亮的元素索引"""
        highlighted = []
        
        if self.current_step < len(self.search_result.steps):
            for i in range(self.current_step + 1):
                step = self.search_result.steps[i]
                if step.index is not None:
                    highlighted.append(step.index)
        
        return highlighted
    
    def next_step(self) -> bool:
        """下一步"""
        if self.current_step < len(self.search_result.steps) - 1:
            self.current_step += 1
            return True
        return False
    
    def previous_step(self) -> bool:
        """上一步"""
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False
    
    def reset(self):
        """重置到第一步"""
        self.current_step = 0
    
    def get_step_info(self) -> Dict[str, Any]:
        """获取当前步骤信息"""
        if not self.search_result or self.current_step >= len(self.search_result.steps):
            return {}
        
        step = self.search_result.steps[self.current_step]
        
        info = {
            "步骤": self.current_step + 1,
            "总步骤": len(self.search_result.steps),
            "操作": step.action,
            "比较结果": step.comparison if step.comparison else "无"
        }
        
        if step.index is not None:
            info["索引"] = step.index
        if step.value is not None:
            info["值"] = step.value
        if step.found:
            info["状态"] = "找到目标！"
        
        return info


class PerformanceVisualizer:
    """性能可视化器"""
    
    @staticmethod
    def create_comparison_chart(df: pd.DataFrame, metric: str = "平均时间(ms)") -> go.Figure:
        """创建性能对比图表"""
        fig = px.bar(
            df, 
            x="算法名称", 
            y=metric,
            color="数据结构",
            barmode="group",
            title=f"算法性能对比 - {metric}"
        )
        
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def create_complexity_chart(df: pd.DataFrame, title: str = "复杂度分析") -> go.Figure:
        """创建复杂度分析图表"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df["数据规模"],
            y=df["平均比较次数"],
            mode='lines+markers',
            name='平均比较次数',
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            x=df["数据规模"],
            y=df["平均时间(ms)"],
            mode='lines+markers',
            name='平均时间(ms)',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="数据规模",
            yaxis=dict(title="比较次数", side="left"),
            yaxis2=dict(title="时间(ms)", side="right", overlaying="y"),
            height=500
        )
        
        return fig
