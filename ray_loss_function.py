from typing import Dict
from embiggen import CSFGraph, N2vGraph
from runLinkPrediction_ppi import read_graphs, get_random_walks


space = {
    "p": (0.5, 1.0), # (float)
    "q": (0.5, 1.0), # (float)
    "num_walks": (10, 100), # (int) This should be dependant on the graph size.
    "walk_length": (5, 100), # (int)
    "embedding_size": (10, 1000), # (int)
    "context_window": (1, 5), # (int)
    "num_epochs": (1, 5) # (int)
}

config = dict(
    paths=dict(
        pos_train="path/to/my/pos_train",
        pos_valid="path/to/my/pos_valid",
        pos_test="path/to/my/pos_test",
        neg_train="path/to/my/neg_train",
        neg_valid="path/to/my/neg_valid",
        neg_tes="path/to/my/neg_tes"
    ),
    w2v_model="skipgram"
)


def custom_loss(config: Dict, reporter):
    pos_train, pos_valid, pos_test, neg_train, neg_valid, neg_test = read_graphs(
        **config["paths"]
    )
    walks = get_random_walks(
        pos_train,
        config["p"],
        config["q"],
        config["num_walks"],
        config["walk_length"]
    )

    reporter(my_custom_loss=x**2)
