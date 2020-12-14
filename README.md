# DGL Implementation of the SAGPool Paper

This DGL example implements the GNN model proposed in the paper [Self Attention Graph Pooling](https://arxiv.org/pdf/1904.08082.pdf). 
The author's codes of implementation is in [here](https://github.com/inyeoplee77/SAGPool)


Example implementor
----------------------
This example was implemented by [Tianqi Zhang](https://github.com/lygztq) during his Applied Scientist Intern work at the AWS Shanghai AI Lab.


The graph dataset used in this example 
---------------------------------------
The DGL's built-in TUDataset. This is a serial of graph kernel datasets for graph classification. We use 'DD', 'PROTEINS', 'NCI1', 'NCI109' and 'FRANKENSTEIN' in this SAGPool implementation. All these datasets are randomly splited to train, validation and test set with ratio 0.8, 0.1 and 0.1.

DD
- NumGraphs: 1178
- AvgNodesPerGraph: 284.32
- AvgEdgesPerGraph: 715.66
- NumFeats: 1
- NumClasses: 2

NOTE: Since there is no data attributes in DD dataset, we use node_id (in one-hot vector whose length is the max number of nodes across all graphs) as the node feature. The one-hot vector size should be 89. Also note that the node_id in this dataset is not unique (e.g. a graph may has two nodes with the same id).

PROTEINS
- NumGraphs: 1113
- AvgNodesPerGraph: 39.06
- AvgEdgesPerGraph: 72.82
- NumFeats: 1
- NumClasses: 2

NCI1
- NumGraphs: 4110
- AvgNodesPerGraph: 29.87
- AvgEdgesPerGraph: 32.30
- NumFeats: 1
- NumClasses: 2

NCI109
- NumGraphs: 4127
- AvgNodesPerGraph: 29.68
- AvgEdgesPerGraph: 32.13
- NumFeats: 1
- NumClasses: 2

FRANKENSTEIN
- NumGraphs: 4337
- AvgNodesPerGraph: 16.90
- AvgEdgesPerGraph: 17.88
- NumFeats: 1
- NumClasses: 2


How to run example files
--------------------------------
In the SAGPool-DGL folder, run

```python
python main.py
```

If want to use a GPU, run

```python
python main.py --gpu 0
```

**Note**：Please replace these commands with your implementation's real commands.

Performance
-------------------------
**Note**: If your implementation needs to reproduce the SOTA performance, please put these performance here.
