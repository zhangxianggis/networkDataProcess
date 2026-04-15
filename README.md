# 网络数据处理项目

该项目用于处理和合并多个 Excel 文件中的网络数据，生成统一的边列表用于网络分析。

## 功能特点

- **数据预处理**：清理、过滤和归一化原始网络数据
- **网络合并**：合并生态、经济、社会三张网络表
- **加权求和**：对跨网络的边值进行加权求和
- **阈值筛选**：根据合并权重筛选重要边
- **输出格式化**：生成标准边列表格式（source, target, weight）

## 项目结构

```
networkDataProcess/
├── input/                # 原始输入数据（Git 不追踪）
│   ├── eco_network.xlsx   # 生态网络数据
│   ├── econ_network.xlsx  # 经济网络数据
│   └── soc_network.xlsx   # 社会网络数据
├── result/               # 生成的输出文件（Git 不追踪）
│   ├── normalized_*.xlsx      # 归一化后的各网络数据
│   ├── combined_network.xlsx   # 合并后的网络数据
│   └── edges.xlsx             # 最终边列表输出
├── combineNetwork.py     # 合并网络的主脚本
├── normalizeNetwork.py   # 归一化处理脚本
├── excel_processor.py    # Excel 处理工具函数
├── .gitignore            # Git 忽略配置
└── README.md             # 项目说明文档
```

## 环境要求

- Python 3.x
- pandas

安装依赖：

```bash
pip install pandas
```

## 使用方法

### 步骤 1：准备输入数据

将网络 Excel 文件放入 `input/` 目录。每个文件应包含三列：

- `from_id`: 源节点 ID
- `to_id`: 目标节点 ID
- `value`: 边的权重/值

### 步骤 2：归一化处理

对原始数据进行归一化处理：

```bash
python normalizeNetwork.py
```

这将在 `result/` 目录生成归一化后的文件：`normalized_eco_network.xlsx`、`normalized_econ_network.xlsx`、`normalized_soc_network.xlsx`

### 步骤 3：合并网络

使用加权求和合并三张网络：

```bash
python combineNetwork.py
```

## 配置参数

### normalizeNetwork.py

无需额外配置，自动处理 `input/` 目录下的所有 Excel 文件。

### combineNetwork.py

```python
# 各网络的权重配置（生态、经济、社会）
DEFAULT_WEIGHTS = [1, 1, 1]

# 边筛选阈值（只保留权重高于此值的边）
DEFAULT_THRESHOLD = 0.01

# 要处理的网络文件（位于 result/ 目录）
NETWORK_FILES = [
    'normalized_eco_network.xlsx',
    'normalized_econ_network.xlsx',
    'normalized_soc_network.xlsx'
]
```

## 输出结果

### 归一化输出文件

`result/normalized_*.xlsx` 包含以下列：
| 列名 | 描述 |
|------|------|
| from_id | 源节点 ID（确保大于 to_id） |
| to_id | 目标节点 ID |
| value | 原始值 |
| normalized_value | 归一化后的值（范围 [0, 1]） |

### 最终输出文件：`result/edges.xlsx`

| 列名   | 描述           |
| ------ | -------------- |
| source | 源节点 ID      |
| target | 目标节点 ID    |
| weight | 合并后的加权值 |

## 处理流程

1. **归一化阶段**：
    - 读取原始网络数据
    - 确保（from_id, to_id）顺序一致（from_id > to_id）
    - 去除重复边
    - 对 value 进行最小-最大归一化

2. **合并阶段**：
    - 读取归一化后的网络文件
    - 应用权重并对每条边的值求和
    - 根据阈值筛选边
    - 重命名列为标准边列表格式

## 示例输出

```
   source  target    weight
0       2       1  0.282871
1       3       1  0.153445
2       3       2  0.333870
3       4       1  0.981100
...
```

## 许可证

本项目仅供内部使用。

## 贡献

欢迎根据需要修改脚本。
