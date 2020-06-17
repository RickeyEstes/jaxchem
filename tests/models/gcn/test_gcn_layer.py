import unittest

import haiku as hk
import jax.random as jrandom
from jaxchem.models import GCNLayer


# params
in_feats = 64
out_feats = 32
batch_size = 32
max_node_size = 30


class TestGCNlayer(unittest.TestCase):
    """Test GCNLayer"""

    def setup_method(self, method):
        self.key = hk.PRNGSequence(1234)
        self.input_data = self.__setup_data()

    def __setup_data(self):
        batched_node_feats = jrandom.normal(next(self.key), (batch_size, max_node_size, in_feats))
        batched_adj = jrandom.normal(next(self.key), (batch_size, max_node_size, max_node_size))
        return (batched_node_feats, batched_adj, True)

    def __forward(self, node_feats, adj, is_training):
        model = GCNLayer(in_feats=in_feats, out_feats=out_feats)
        return model(node_feats, adj, is_training)

    def test_forward_shape(self):
        """Test output shape of GCNLayer"""
        forward = hk.transform(self.__forward, apply_rng=True)
        params = forward.init(next(self.key), *self.input_data)
        preds = forward.apply(params, next(self.key), *self.input_data)
        assert preds.shape == (batch_size, max_node_size, out_feats)
