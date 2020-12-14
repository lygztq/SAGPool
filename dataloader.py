import torch.utils.data
from torch.utils.data.dataloader import DataLoader



class GraphDataLoader(torch.utils.data.DataLoader):
    def __init__(self, dataset, batch_size=1, shuffle=False, **kwargs):
        super(GraphDataLoader, self).__init__(dataset, batch_size, shuffle,
                                              collate_fn=None, **kwargs)
