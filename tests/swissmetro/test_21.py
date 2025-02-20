import os
import unittest
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme.expressions import Beta, bioNormalCdf, Elem, log


myPath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(f'{myPath}/swissmetro.dat', sep='\t')
database = db.Database('swissmetro', df)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
# print(database.data.describe())

globals().update(database.variables)

# As we estimate a binary model, we remove observations where
# Swissmetro was chosen (CHOICE == 2). We also remove observations
# where one of the two alternatives is not available.

CAR_AV_SP = database.DefineVariable('CAR_AV_SP', CAR_AV * (SP != 0))
TRAIN_AV_SP = database.DefineVariable('TRAIN_AV_SP', TRAIN_AV * (SP != 0))
exclude = (TRAIN_AV_SP == 0) + (CAR_AV_SP == 0) + (CHOICE == 2) + (
    (PURPOSE != 1) * (PURPOSE != 3) + (CHOICE == 0)
) > 0


database.remove(exclude)


ASC_CAR = Beta('ASC_CAR', 1, None, None, 0)
B_TIME = Beta('B_TIME', 1, None, None, 0)
B_COST = Beta('B_COST', 1, None, None, 0)


TRAIN_COST = TRAIN_CO * (GA == 0)

TRAIN_TT_SCALED = database.DefineVariable('TRAIN_TT_SCALED', TRAIN_TT / 100.0)
TRAIN_COST_SCALED = database.DefineVariable(
    'TRAIN_COST_SCALED', TRAIN_COST / 100
)
CAR_TT_SCALED = database.DefineVariable('CAR_TT_SCALED', CAR_TT / 100)
CAR_CO_SCALED = database.DefineVariable('CAR_CO_SCALED', CAR_CO / 100)

# We estimate a binary probit model. There are only two alternatives.
V1 = B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED
V3 = ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED

# Associate choice probability with the numbering of alternatives

P = {1: bioNormalCdf(V1 - V3), 3: bioNormalCdf(V3 - V1)}


prob = Elem(P, CHOICE)


class test_02(unittest.TestCase):
    def testEstimation(self):
        biogeme = bio.BIOGEME(database, log(prob))
        biogeme.saveIterations = False
        biogeme.generateHtml = False
        biogeme.generatePickle = False
        results = biogeme.estimate()
        self.assertAlmostEqual(results.data.logLike, -986.1888, 2)


if __name__ == '__main__':
    unittest.main()
