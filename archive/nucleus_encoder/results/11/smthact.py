import lasagne
import theano.tensor as T
import numpy as np

# The input must be flattened
class SmthAct1Layer(lasagne.layers.Layer):
    def __init__(self, incoming, x_start, x_end, num_segs, W = lasagne.init.Normal(std = 0.01, mean = 0.1), **kwargs):
        super(SmthAct1Layer, self).__init__(incoming, **kwargs);
        num_inputs = self.input_shape[1];

        self.x_start = x_start;
        self.x_end = x_end;
        self.x_step = (x_end - x_start) / num_segs;
        self.num_segs = num_segs;

        self.W = self.add_param(W, (num_segs, num_inputs), name = 'W', small_weights = True, regularizable = True);

    def basisf(self, x, s, e):
        cpstart = T.le(s, x);
        cpend = T.gt(e, x);
        return 0 * (1 - cpstart) + (x - s) * cpstart * cpend + (e - s) * (1 - cpend);

    def get_output_for(self, input, **kwargs):
        output = T.zeros_like(input);
        for seg in range(0, self.num_segs):
            output += self.basisf(input, self.x_start + self.x_step * seg, self.x_start + self.x_step * (seg + 1)) * self.W[seg, :];

        return output;


class SmthAct2Layer(lasagne.layers.Layer):
    def __init__(self, incoming, x_start, x_end, num_segs, W = lasagne.init.Normal(std = 0.01, mean = 0.1), **kwargs):
        super(SmthAct2Layer, self).__init__(incoming, **kwargs);
        num_inputs = self.input_shape[1];

        self.x_start = x_start;
        self.x_end = x_end;
        self.x_step = (x_end - x_start) / num_segs;
        self.num_segs = num_segs;

        self.W = self.add_param(W, (num_segs, num_inputs), name = 'W', small_weights = True, regularizable = True);

    def basisf(self, x, s, e):
        cpstart = T.le(s, x);
        cpend = T.gt(e, x);
        return 0 * (1 - cpstart) + 0.5 * (x - s)**2 * cpstart * cpend + ((e - s) * (x - e) + 0.5 * (e - s)**2) * (1 - cpend);

    def get_output_for(self, input, **kwargs):
        output = T.zeros_like(input);
        for seg in range(0, self.num_segs):
            output += self.basisf(input, self.x_start + self.x_step * seg, self.x_start + self.x_step * (seg + 1)) * self.W[seg, :];

        return output;

