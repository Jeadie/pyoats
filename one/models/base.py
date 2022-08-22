from typing import Protocol
import numpy.typing as npt
import numpy as np


class Model(Protocol):
    def fit(self):
        raise NotImplementedError

    def get_scores(self):
        raise NotImplementedError

    @property
    def model_name(self):
        name = type(self).__name__
        if self.rnn_model:
            return f"{name}_{self.rnn_model}"

        return name

    def _handle_multivariate(self, data, models):
        scores = []
        for idx, series in enumerate(data.T):
            scores.append(models[idx].get_scores(series))

        return np.array(scores).T

    def _pseudo_mv_train(self, data):
        models = []
        for _ in range(data.shape[1]):
            models.append(self.__class__(**self.__dict__))
        
        for idx, series in enumerate(data.T):
            models[idx].fit(series)

        return models