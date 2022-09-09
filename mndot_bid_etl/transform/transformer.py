from functools import reduce
import pandas as pd
from dataclasses import dataclass

from .transformation import TransformationFunction


@dataclass
class Transformer:
    """
    Provides and apply method that executes a sequence of transformation functions on a dataframe.

    Parameters
    ----------
    transformation_functions : ordered list of TransformationFunction
        TransformationFunction : function that receive a dataframe as an argument and return a modified dataframe
    """

    transformation_functions: list[TransformationFunction]

    def __post_init__(self) -> None:
        """Reduce the list of TransformationFunctions to a single function."""
        self.reduced_transformation = reduce(
            lambda f, g: lambda x: g(f(x)), self.transformation_functions
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.pipe(self.reduced_transformation)
