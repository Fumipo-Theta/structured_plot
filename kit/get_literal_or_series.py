from ..plot_action.mapping import IGetSeriesOrLiteral
from ..type_set import LiteralOrSequencer, LiteralOrSequence, DataSource


def get_literal_or_series(input: LiteralOrSequencer, df: DataSource)->LiteralOrSequence:

    if isinstance(input, IGetSeriesOrLiteral):
        return input.apply(df)
    elif callable(input):
        return input(df)
    else:
        return input
