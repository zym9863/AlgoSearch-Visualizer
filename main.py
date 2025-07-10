"""
算法查找可视化分析器主应用
整合所有功能模块，创建完整的Streamlit应用界面
"""

import streamlit as st
import pandas as pd
import random
from typing import List, Any

# 导入自定义模块
from data_structures import create_data_structure, SearchableArray, SearchableLinkedList, BinarySearchTree
from search_algorithms import SearchAlgorithmFactory, SearchResult
from performance_testing import BenchmarkSuite, PerformanceTester
from visualization import DataStructureVisualizer, SearchVisualizationController, PerformanceVisualizer


def main():
    """主函数"""
    st.set_page_config(
        page_title="算法查找可视化分析器",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🔍 算法查找可视化分析器")
    st.markdown("---")

    # 侧边栏导航
    st.sidebar.title("功能导航")
    page = st.sidebar.selectbox(
        "选择功能模块",
        ["交互式查找可视化", "性能基准测试", "复杂度分析", "关于项目"]
    )

    if page == "交互式查找可视化":
        interactive_search_page()
    elif page == "性能基准测试":
        performance_testing_page()
    elif page == "复杂度分析":
        complexity_analysis_page()
    elif page == "关于项目":
        about_page()


def interactive_search_page():
    """交互式查找可视化页面"""
    st.header("🎯 交互式查找过程可视化")

    # 配置区域
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("配置参数")

        # 数据结构选择
        ds_type = st.selectbox(
            "选择数据结构",
            ["array", "linked_list", "binary_search_tree"],
            format_func=lambda x: {
                "array": "数组",
                "linked_list": "链表",
                "binary_search_tree": "二叉搜索树"
            }[x]
        )

        # 算法选择
        available_algorithms = get_compatible_algorithms(ds_type)
        algorithm = st.selectbox(
            "选择查找算法",
            available_algorithms,
            format_func=lambda x: {
                "linear": "线性查找",
                "binary": "二分查找",
                "bst": "二叉搜索树查找"
            }[x]
        )

        # 数据配置
        st.subheader("数据配置")
        data_source = st.radio("数据来源", ["随机生成", "手动输入"])

        if data_source == "随机生成":
            data_size = st.slider("数据规模", 5, 50, 15)
            min_val = st.number_input("最小值", value=1)
            max_val = st.number_input("最大值", value=100)

            if st.button("生成随机数据"):
                data_structure = create_data_structure(ds_type)
                data_structure.generate_random_data(data_size, min_val, max_val)

                # 对于二分查找，需要排序
                if algorithm == "binary" and hasattr(data_structure, 'sort'):
                    data_structure.sort()

                st.session_state.data_structure = data_structure
                st.success("数据生成成功！")

        else:
            data_input = st.text_input(
                "输入数据（用逗号分隔）",
                placeholder="例如: 1,3,5,7,9,11"
            )

            if st.button("创建数据结构"):
                try:
                    data = [int(x.strip()) for x in data_input.split(',') if x.strip()]
                    data_structure = create_data_structure(ds_type, data)

                    # 对于二分查找，需要排序
                    if algorithm == "binary" and hasattr(data_structure, 'sort'):
                        data_structure.sort()

                    st.session_state.data_structure = data_structure
                    st.success("数据结构创建成功！")
                except ValueError:
                    st.error("请输入有效的数字序列")

        # 查找目标
        if 'data_structure' in st.session_state:
            st.subheader("查找目标")
            target = st.number_input("目标值", value=1)

            if st.button("开始查找", type="primary"):
                try:
                    result = SearchAlgorithmFactory.search(
                        algorithm,
                        st.session_state.data_structure,
                        target
                    )

                    # 初始化可视化控制器
                    controller = SearchVisualizationController()
                    controller.setup_search(
                        st.session_state.data_structure,
                        target,
                        result
                    )

                    st.session_state.search_controller = controller
                    st.session_state.search_result = result
                    st.success("查找完成！")

                except Exception as e:
                    st.error(f"查找出错: {e}")

    with col2:
        st.subheader("可视化展示")

        # 显示当前数据结构
        if 'data_structure' in st.session_state:
            ds = st.session_state.data_structure

            # 显示数据结构信息
            if isinstance(ds, SearchableArray):
                st.info(f"数组数据: {ds.data}")
            elif isinstance(ds, SearchableLinkedList):
                st.info(f"链表数据: {ds.to_list()}")
            elif isinstance(ds, BinarySearchTree):
                st.info(f"二叉搜索树数据: {ds.inorder_traversal()}")

            # 显示可视化
            if 'search_controller' in st.session_state:
                controller = st.session_state.search_controller

                # 控制按钮
                col_prev, col_next, col_reset = st.columns(3)

                with col_prev:
                    if st.button("⬅️ 上一步"):
                        controller.previous_step()

                with col_next:
                    if st.button("➡️ 下一步"):
                        controller.next_step()

                with col_reset:
                    if st.button("🔄 重置"):
                        controller.reset()

                # 显示当前步骤信息
                step_info = controller.get_step_info()
                if step_info:
                    st.json(step_info)

                # 显示可视化图表
                fig = controller.get_current_visualization()
                st.plotly_chart(fig, use_container_width=True)

                # 显示查找结果摘要
                if 'search_result' in st.session_state:
                    result = st.session_state.search_result

                    col_found, col_time, col_comparisons = st.columns(3)

                    with col_found:
                        status = "✅ 找到" if result.found else "❌ 未找到"
                        st.metric("查找结果", status)

                    with col_time:
                        st.metric("耗时", f"{result.time_taken * 1000:.4f} ms")

                    with col_comparisons:
                        st.metric("比较次数", result.comparisons)

            else:
                # 显示静态数据结构
                if isinstance(ds, SearchableArray):
                    fig = DataStructureVisualizer.visualize_array(ds)
                elif isinstance(ds, SearchableLinkedList):
                    fig = DataStructureVisualizer.visualize_linked_list(ds)
                elif isinstance(ds, BinarySearchTree):
                    fig = DataStructureVisualizer.visualize_binary_tree(ds)

                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("请先配置并生成数据结构")


def get_compatible_algorithms(ds_type: str) -> List[str]:
    """获取与数据结构兼容的算法"""
    compatibility = {
        "array": ["linear", "binary"],
        "linked_list": ["linear"],
        "binary_search_tree": ["bst"]
    }
    return compatibility.get(ds_type, [])


def performance_testing_page():
    """性能基准测试页面"""
    st.header("📊 多算法性能基准测试")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("测试配置")

        # 选择要测试的算法
        st.write("选择测试算法:")
        test_linear = st.checkbox("线性查找", value=True)
        test_binary = st.checkbox("二分查找", value=True)
        test_bst = st.checkbox("二叉搜索树查找", value=True)

        # 选择数据结构
        st.write("选择数据结构:")
        test_array = st.checkbox("数组", value=True)
        test_linked_list = st.checkbox("链表", value=True)
        test_tree = st.checkbox("二叉搜索树", value=True)

        # 测试参数
        st.subheader("测试参数")
        data_sizes = st.multiselect(
            "数据规模",
            [100, 500, 1000, 2000, 5000],
            default=[100, 500, 1000]
        )

        test_count = st.slider("每组测试次数", 10, 200, 50)

        if st.button("开始性能测试", type="primary"):
            # 构建测试配置
            algorithms = []
            if test_linear:
                algorithms.append("linear")
            if test_binary:
                algorithms.append("binary")
            if test_bst:
                algorithms.append("bst")

            data_structures = []
            if test_array:
                data_structures.append("array")
            if test_linked_list:
                data_structures.append("linked_list")
            if test_tree:
                data_structures.append("binary_search_tree")

            if algorithms and data_structures and data_sizes:
                with st.spinner("正在执行性能测试..."):
                    tester = PerformanceTester()
                    results = tester.batch_test(algorithms, data_structures, data_sizes, test_count)

                    # 生成报告
                    report_df = tester.generate_comparison_report()
                    best_by_time = tester.get_best_algorithm_by_metric("avg_time")
                    best_by_comparisons = tester.get_best_algorithm_by_metric("avg_comparisons")

                    st.session_state.performance_results = {
                        "report": report_df,
                        "best_by_time": best_by_time,
                        "best_by_comparisons": best_by_comparisons
                    }

                st.success("性能测试完成！")
            else:
                st.error("请至少选择一个算法、一个数据结构和一个数据规模")

    with col2:
        st.subheader("测试结果")

        if 'performance_results' in st.session_state:
            results = st.session_state.performance_results

            # 显示详细报告
            st.subheader("详细性能报告")
            st.dataframe(results["report"], use_container_width=True)

            # 性能对比图表
            st.subheader("性能对比图表")

            # 时间对比
            if not results["report"].empty:
                # 转换数据用于绘图
                df_plot = results["report"].copy()
                df_plot["平均时间(ms)"] = df_plot["平均时间(ms)"].str.replace(" ms", "").astype(float)

                fig_time = PerformanceVisualizer.create_comparison_chart(
                    df_plot, "平均时间(ms)"
                )
                st.plotly_chart(fig_time, use_container_width=True)

                # 比较次数对比
                df_plot["平均比较次数"] = df_plot["平均比较次数"].astype(float)
                fig_comparisons = PerformanceVisualizer.create_comparison_chart(
                    df_plot, "平均比较次数"
                )
                st.plotly_chart(fig_comparisons, use_container_width=True)

            # 最佳算法推荐
            st.subheader("最佳算法推荐")

            col_time, col_comparisons = st.columns(2)

            with col_time:
                st.write("**按时间性能:**")
                for group, info in results["best_by_time"].items():
                    st.write(f"- {group}: {info['algorithm']}")

            with col_comparisons:
                st.write("**按比较次数:**")
                for group, info in results["best_by_comparisons"].items():
                    st.write(f"- {group}: {info['algorithm']}")

        else:
            st.info("请配置测试参数并开始测试")


def complexity_analysis_page():
    """复杂度分析页面"""
    st.header("📈 算法复杂度分析")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("分析配置")

        # 选择算法和数据结构组合
        analysis_type = st.selectbox(
            "选择分析类型",
            ["linear_array", "binary_array", "bst_tree"],
            format_func=lambda x: {
                "linear_array": "线性查找 - 数组",
                "binary_array": "二分查找 - 数组",
                "bst_tree": "BST查找 - 二叉搜索树"
            }[x]
        )

        # 数据规模范围
        st.subheader("数据规模范围")
        min_size = st.number_input("最小规模", value=50, min_value=10)
        max_size = st.number_input("最大规模", value=2000, min_value=100)
        step_size = st.number_input("步长", value=200, min_value=50)

        test_count = st.slider("每个规模测试次数", 10, 100, 30)

        if st.button("开始复杂度分析", type="primary"):
            size_range = list(range(min_size, max_size + 1, step_size))

            with st.spinner("正在进行复杂度分析..."):
                tester = PerformanceTester()

                if analysis_type == "linear_array":
                    df = tester.complexity_analysis("linear", "array", size_range, test_count)
                elif analysis_type == "binary_array":
                    df = tester.complexity_analysis("binary", "array", size_range, test_count)
                elif analysis_type == "bst_tree":
                    df = tester.complexity_analysis("bst", "binary_search_tree", size_range, test_count)

                st.session_state.complexity_analysis = {
                    "data": df,
                    "type": analysis_type
                }

            st.success("复杂度分析完成！")

    with col2:
        st.subheader("分析结果")

        if 'complexity_analysis' in st.session_state:
            analysis = st.session_state.complexity_analysis
            df = analysis["data"]
            analysis_type = analysis["type"]

            # 显示数据表
            st.subheader("详细数据")
            st.dataframe(df, use_container_width=True)

            # 复杂度图表
            st.subheader("复杂度趋势图")

            algorithm_name = {
                "linear_array": "线性查找 - 数组",
                "binary_array": "二分查找 - 数组",
                "bst_tree": "BST查找 - 二叉搜索树"
            }[analysis_type]

            fig = PerformanceVisualizer.create_complexity_chart(
                df, f"{algorithm_name} 复杂度分析"
            )
            st.plotly_chart(fig, use_container_width=True)

            # 理论复杂度对比
            st.subheader("理论复杂度")

            complexity_info = {
                "linear_array": {
                    "时间复杂度": "O(n)",
                    "空间复杂度": "O(1)",
                    "最好情况": "O(1) - 第一个元素就是目标",
                    "最坏情况": "O(n) - 目标在最后或不存在"
                },
                "binary_array": {
                    "时间复杂度": "O(log n)",
                    "空间复杂度": "O(1)",
                    "最好情况": "O(1) - 中间元素就是目标",
                    "最坏情况": "O(log n) - 需要完整的二分过程"
                },
                "bst_tree": {
                    "时间复杂度": "O(log n) 平均, O(n) 最坏",
                    "空间复杂度": "O(log n) 递归栈",
                    "最好情况": "O(1) - 根节点就是目标",
                    "最坏情况": "O(n) - 树退化为链表"
                }
            }

            info = complexity_info[analysis_type]
            for key, value in info.items():
                st.write(f"**{key}**: {value}")

        else:
            st.info("请配置分析参数并开始分析")


def about_page():
    """关于项目页面"""
    st.header("📖 关于项目")

    st.markdown("""
    ## 🔍 算法查找可视化分析器

    这是一个专门用于学习和分析查找算法的交互式可视化工具。

    ### ✨ 核心功能

    #### 1. 交互式查找过程可视化
    - 支持多种数据结构：数组、链表、二叉搜索树
    - 实现多种查找算法：线性查找、二分查找、二叉搜索树查找
    - 逐步动态展示算法执行过程
    - 高亮显示当前比较的元素
    - 用不同颜色标记已访问和未访问的节点

    #### 2. 多算法性能基准测试
    - 批量执行查找操作
    - 自动记录关键性能指标
    - 横向对比不同算法的性能
    - 生成详细的性能报告

    #### 3. 复杂度分析
    - 分析算法在不同数据规模下的表现
    - 可视化时间复杂度和比较次数趋势
    - 对比理论复杂度与实际测试结果

    ### 🛠️ 技术栈
    - **Python**: 核心编程语言
    - **Streamlit**: Web界面框架
    - **Plotly**: 交互式图表库
    - **Pandas**: 数据处理
    - **NumPy**: 数值计算

    ### 🎯 教育价值
    - 帮助初学者直观理解抽象的查找算法
    - 看清算法的内部工作原理和逻辑流程
    - 量化感知不同算法的性能差异
    - 深刻理解时间复杂度和适用场景

    ### 🚀 使用建议
    1. 从**交互式查找可视化**开始，理解算法基本原理
    2. 使用**性能基准测试**对比不同算法的效率
    3. 通过**复杂度分析**深入理解算法的扩展性

    ### 📝 开发信息
    - 版本: 1.0.0
    - 开发者: AI编程助手
    - 开源协议: MIT License
    """)


if __name__ == "__main__":
    main()
