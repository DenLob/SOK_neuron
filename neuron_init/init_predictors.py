from neuron_init.bbox_ph_init import bbox_ph_init
from neuron_init.decr_ph_init import decr_ph_init


def init_predictors():
    return [decr_ph_init(), bbox_ph_init()]