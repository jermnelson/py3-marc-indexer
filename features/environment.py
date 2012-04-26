__author__ = "Jeremy Nelson"

def before_feature(context,feature):
    """
    Function sets up context's MARC file

    :param context: Context
    :param feature: Feature
    """
    context.marc_record = None
