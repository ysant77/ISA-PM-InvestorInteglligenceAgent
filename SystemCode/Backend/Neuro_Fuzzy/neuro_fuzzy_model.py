from keras import layers, models
import numpy as np
import keras
import tensorflow as tf
from keras.models import load_model

class FuzzificationLayer(layers.Layer):
    def __init__(self, num_variables, num_sets, **kwargs):
        super(FuzzificationLayer, self).__init__(**kwargs)
        self.num_variables = num_variables
        self.num_sets = num_sets
        self.means = self.add_weight(name='means',
                                     shape=(num_variables, num_sets),
                                     initializer='random_normal',
                                     trainable=True)
        self.sigmas = self.add_weight(name='sigmas',
                                      shape=(num_variables, num_sets),
                                      initializer='random_normal',
                                      trainable=True)

    def call(self, inputs):
        tmp = tf.exp(-0.5 * tf.square((tf.expand_dims(inputs, -1) - self.means) / self.sigmas))
        return tmp

    def get_config(self):
        config = super(FuzzificationLayer, self).get_config()
        config.update({
            'num_variables': self.num_variables,
            'num_sets': self.num_sets
        })
        return config
    
class RuleApplicationLayer(layers.Layer):
    def __init__(self, num_classes, num_variables, num_rules, **kwargs):
        super(RuleApplicationLayer, self).__init__(**kwargs)
        self.num_classes = num_classes
        self.num_variables = num_variables
        self.num_rules = num_rules
        self.rule_combination_layer = layers.Dense(num_rules, use_bias=False, activation='sigmoid')

    def call(self, fuzzified_inputs):
        num_features = self.num_variables * self.num_classes
        reshaped_inputs = tf.reshape(fuzzified_inputs, [-1, num_features])
        rule_firing_strengths = self.rule_combination_layer(reshaped_inputs)
        return rule_firing_strengths

    def get_config(self):
        config = super(RuleApplicationLayer, self).get_config()
        config.update({
            'num_classes': self.num_classes,
            'num_variables': self.num_variables,
            'num_rules': self.num_rules
        })
        return config

class DefuzzificationLayer(layers.Layer):
    def __init__(self, num_rules, num_classes, **kwargs):
        super(DefuzzificationLayer, self).__init__(**kwargs)
        self.num_rules = num_rules
        self.num_classes = num_classes
        self.rule_weights = self.add_weight(name='rule_weights',
                                            shape=(num_rules, num_classes),
                                            initializer='random_normal',
                                            trainable=True)

    def call(self, rule_outputs):
        weighted_sum = tf.matmul(rule_outputs, self.rule_weights)
        return weighted_sum

    def get_config(self):
        config = super(DefuzzificationLayer, self).get_config()
        config.update({
            'num_rules': self.num_rules,
            'num_classes': self.num_classes
        })
        return config

@keras.saving.register_keras_serializable(package="MyLayers")

class ANFISModel(models.Model):
    def __init__(self, num_variables, num_sets, num_rules, num_classes, **kwargs):
        super(ANFISModel, self).__init__( **kwargs)
        self.num_variables = num_variables
        self.num_sets = num_sets
        self.num_rules = num_rules
        self.num_classes = num_classes
        self.fuzzification_layer = FuzzificationLayer(num_variables, num_sets)
        self.rule_application_layer = RuleApplicationLayer(num_classes, num_variables, num_rules)
        self.defuzzification_layer = DefuzzificationLayer(num_rules, num_classes)

    def call(self, inputs):
        fuzzified = self.fuzzification_layer(inputs)
        rule_applied = self.rule_application_layer(fuzzified)
        logits = self.defuzzification_layer(rule_applied)
        return tf.nn.softmax(logits)  # Use softmax to convert logits to probabilities

    def get_config(self):
        config = super(ANFISModel, self).get_config()
        config.update({
            'num_variables': self.num_variables,
            'num_sets': self.num_sets,
            'num_rules': self.num_rules,
            'num_classes': self.num_classes,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)

class ModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path
    
    def load_model(self):
        with tf.keras.utils.custom_object_scope({'ANFISModel': ANFISModel}):
            self.model = load_model(self.model_path)
        return self.model
