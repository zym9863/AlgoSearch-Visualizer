[English](README_EN.md) | [中文](README.md)

# 🔍 Algorithm Search Visualizer

An interactive visualization tool designed for learning and analyzing search algorithms, helping beginners and developers intuitively understand abstract search algorithms.

## ✨ Core Features

### 1. Interactive Search Process Visualization
- **Multiple Data Structures Supported**: Array, Linked List, Binary Search Tree
- **Multiple Search Algorithms**: Linear Search, Binary Search, BST Search
- **Step-by-Step Dynamic Display**: Visualize every step of the algorithm execution
- **Smart Highlighting**: Highlight the currently compared element
- **State Marking**: Use different colors to mark visited and unvisited nodes

### 2. Multi-Algorithm Performance Benchmarking
- **Batch Testing**: Test multiple algorithms on different data scales simultaneously
- **Key Metrics Recording**: Average search time, total comparisons, success rate, etc.
- **Horizontal Comparison**: Clear charts to show performance differences between algorithms
- **Best Recommendation**: Recommend the most suitable algorithm based on different metrics

### 3. Complexity Analysis
- **Scalability Analysis**: Analyze algorithm performance on different data scales
- **Trend Visualization**: Show trends of time complexity and comparison counts
- **Theoretical Comparison**: Compare actual test results with theoretical complexity

## 🛠️ Tech Stack

- **Python 3.12+**: Core programming language
- **uv**: Modern Python package manager
- **Streamlit**: Web UI framework
- **Plotly**: Interactive chart library
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computation support

## 🚀 Quick Start

### Requirements
- Python 3.12 or higher
- uv package manager

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/zym9863/AlgoSearch-Visualizer.git
cd AlgoSearch-Visualizer
```

2. **Install dependencies**
```bash
uv sync
```

3. **Run the application**
```bash
uv run streamlit run main.py
```

4. **Access the app**
Open your browser and visit `http://localhost:8501`

### Run Tests
```bash
uv run python test_algorithms.py
```

## 📖 User Guide

### Interactive Search Visualization
1. Select data structure type (Array, Linked List, Binary Search Tree)
2. Select the corresponding search algorithm
3. Configure data (randomly generated or manually input)
4. Enter the target value to search
5. Click "Start Search" to watch the visualization process
6. Use control buttons to step through the algorithm execution

### Performance Benchmarking
1. Select algorithm combinations to test
2. Configure test parameters (data scale, number of tests)
3. Start batch testing
4. View detailed performance reports and comparison charts
5. Get the best algorithm recommendation

### Complexity Analysis
1. Select algorithm and data structure combination
2. Set data scale range
3. Start complexity analysis
4. View trend charts and theoretical complexity comparison

## 📁 Project Structure

```
AlgoSearch-Visualizer/
├── main.py                 # Main application entry
├── data_structures.py      # Data structure implementations
├── search_algorithms.py    # Search algorithm implementations
├── performance_testing.py  # Performance testing module
├── visualization.py        # Visualization components
├── test_algorithms.py      # Unit tests
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

## 🎯 Educational Value

- **Intuitive Understanding**: Visualize to help understand abstract algorithm concepts
- **Performance Awareness**: Quantify performance differences between algorithms
- **Complexity Cognition**: Deepen understanding of time complexity in practice
- **Application Scenarios**: Learn the best use cases for different algorithms

## 🔧 Development Features

- **Modular Design**: Clear code structure, easy to extend
- **Comprehensive Testing**: Full unit tests ensure code quality
- **Type Hints**: Complete type annotations for better readability
- **Chinese UI**: Fully localized Chinese user interface

## 📊 Supported Algorithms

| Algorithm      | Data Structure      | Time Complexity      | Space Complexity |
|---------------|--------------------|---------------------|-----------------|
| Linear Search | Array, Linked List | O(n)                | O(1)            |
| Binary Search | Sorted Array       | O(log n)            | O(1)            |
| BST Search    | Binary Search Tree | O(log n) average    | O(log n)        |

## 🤝 Contribution Guide

Contributions via Issues and Pull Requests are welcome to improve this project!

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgements

Thanks to all developers and educators who contribute to algorithm education.
