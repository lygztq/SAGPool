import torch
import torch.nn
import argparse
import os
import torch.nn.functional as F
from torch.utils.data import random_split
from dgl.data import LegacyTUDataset

from dataloader import GraphDataLoader
from network import get_sag_network


def parse_args():
    parser = argparse.ArgumentParser(description="Self-Attention Graph Pooling")
    parser.add_argument("--dataset", type=str, default="DD",
                        choices=["DD", "PROTEINS", "NCI1", "NCI109", "Mutagenicity"],
                        help="DD/PROTEINS/NCI1/NCI109/Mutagenicity")
    parser.add_argument("--batch_size", type=int, default=128,
                        help="batch size")
    parser.add_argument("--lr", type=float, default=5e-4,
                        help="learning rate")
    parser.add_argument("--weight_decay", type=float, default=1e-4,
                        help="weight decay")
    parser.add_argument("--pool_ratio", type=float, default=0.5,
                        help="pooling ratio")
    parser.add_argument("--hid_dim", type=int, default=128,
                        help="hidden size")
    parser.add_argument("--dropout", type=float, default=0.5,
                        help="dropout ratio")
    parser.add_argument("--epochs", type=int, default=1e5,
                        help="max number of training epochs")
    parser.add_argument("--patience", type=int, default=50,
                        help="patience for early stopping")
    parser.add_argument("--device", type=int, default=-1,
                        help="device id, -1 for cpu")
    parser.add_argument("--architecture", type=str, choices=["hierarchical", "global"],
                        help="model architecture")
    parser.add_argument("--dataset_path", type=str, default="./dataset",
                        help="path to dataset")
    parser.add_argument("--conv_layers", type=int, default=3,
                        help="number of conv layers")
    parser.add_argument("--print_every", type=int, default=10,
                        help="print trainlog every k epochs")
    
    args = parser.parse_args()
    args.device = "cpu" if args.device == -1 else "cuda:{}".format(args.device)
    if not torch.cuda.is_available():
        args.device = "cpu"
    if not os.path.exists(args.dataset_path):
        os.makedirs(args.dataset_path)
    
    return args


def train(model:torch.nn.Module, optimizer, trainloader):
    model.train()
    total_loss = 0.
    for batch in trainloader:
        optimizer.zero_grad()
        batch_graphs, batch_labels = batch
        batch_graphs = batch_graphs.to(model.device)
        out = model(batch_graphs)
        loss = F.nll_loss(out, batch_labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    
    return total_loss / len(trainloader.dataset)


@torch.no_grad()
def test(model:torch.nn.Module, loader):
    model.eval()
    correct = 0.
    loss = 0.
    num_graphs = len(loader.dataset)
    for batch in loader:
        batch_graphs, batch_labels = batch
        batch_graphs = batch_graphs.to(model.device)
        out = model(batch_graphs)
        pred = out.argmax(dim=1)
        loss += F.nll_loss(out, batch_labels, reduction="sum").item()
        correct += pred.eq(batch_labels).sum().item()
    return correct / num_graphs, loss / num_graphs


def main(args):
    # Step 1: Prepare graph data and retrieve train/validation/test index ============================= #
    dataset = LegacyTUDataset(args.dataset, raw_dir=args.dataset_path)
    num_training = int(len(dataset) * 0.8)
    num_val = int(len(dataset) * 0.1)
    num_test = len(dataset) - num_val - num_training
    train_set, val_set, test_set = random_split(dataset, [num_training, num_val, num_test])

    train_loader = GraphDataLoader(train_set, batch_size=args.batch_size, shuffle=True, num_workers=12)
    val_loader = GraphDataLoader(val_set, batch_size=args.batch_size)
    test_loader = GraphDataLoader(test_set, batch_size=args.batch_size)

    device = torch.device(args.device)
    
    # Step 2: Create model =================================================================== #
    num_feature, num_classes, max_num_nodes = dataset.statistics()
    model_op = get_sag_network(args.architecture)
    model = model_op(in_dim=num_feature, hid_dim=args.hid_dim, out_dim=num_classes,
                     num_convs=args.conv_layers, pool_ratio=args.pool_ratio, dropout=args.dropout).to(device)

    # Step 3: Create training components ===================================================== #
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # Step 4: training epoches =============================================================== #
    bad_cound = 0
    best_val_loss = float("inf")
    final_test_acc = 0.
    best_epoch = 0
    for e in range(args.epochs):
        train_loss = train(model, optimizer, train_loader)
        val_acc, val_loss = test(model, val_loader)
        test_acc, _ = test(model, test_loader)
        if best_val_loss > val_loss:
            best_val_loss = val_loss
            final_test_acc = test_acc
            bad_cound = 0
            best_epoch = e + 1
        else:
            bad_cound += 1
        if bad_cound >= args.patience:
            break
        
        if (e + 1) % args.print_every == 0:
            log_format = "Epoch {}: loss={:.4f}, val_acc={:.4f}, final_test_acc={:.4f}"
            print(log_format, e + 1, train_loss, val_acc, final_test_acc)
    print("Best Epoch {}, final test acc {:.4f}".format(best_epoch, final_test_acc))


if __name__ == "__main__":
    args = parse_args()
    main(args)
