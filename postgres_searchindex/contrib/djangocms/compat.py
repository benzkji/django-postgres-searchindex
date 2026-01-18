import cms
from looseversion import LooseVersion

GTE_CMS_35 = LooseVersion(cms.__version__) >= LooseVersion("3.5")
LT_CMS_40 = LooseVersion(cms.__version__) < LooseVersion("4.0")
GTE_CMS_50 = LooseVersion(cms.__version__) >= LooseVersion("5.0")
