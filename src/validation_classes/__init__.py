from __future__ import annotations

from .logsheets import Model as logsheetsModel
from .mandatory import SoftSedimentDataModel as softSedimentMandatoryModel
from .mandatory import WaterColumnDataModel as waterColumnMandatoryModel
from .measured import Model as measuredModel
from .observatories import Model as observatoriesModel
from .observatory import Model as observatoryModel
from .sampling import Model as samplingModel
from .sampling_github import ModelGithub as samplingModelGithub
from .sampling_github import (
    SemiStrictModelGithub as samplingModelGithubSemiStrict,
)
from .sampling_github import StrictModelGithub as samplingModelGithubStrict

__all__ = [
    "logsheetsModel",
    "measuredModel",
    "observatoriesModel",
    "observatoryModel",
    "samplingModel",
    "samplingModelGithub",
    "samplingModelGithubSemiStrict",
    "samplingModelGithubStrict",
    "waterColumnMandatoryModel",
    "softSedimentMandatoryModel",
]
