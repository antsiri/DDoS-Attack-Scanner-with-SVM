import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)
def warn(*args, **kwargs):
	pass
warnings.warn = warn
