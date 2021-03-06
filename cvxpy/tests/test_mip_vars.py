"""
Copyright 2017 Steven Diamond

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from cvxpy import *
from cvxpy.expressions.variables import Bool, Int
from cvxpy.tests.base_test import BaseTest


class TestMIPVariable(BaseTest):
    """ Unit tests for the expressions/shape module. """

    def setUp(self):
        self.x_bool = Bool(name='x')
        self.y_int = Int()
        self.A_bool = Bool(3, 2)
        self.B_int = Int(2, 3, name='B')

    def test_mip_consistency(self):
        """Test that MIP problems are deterministic.
        """
        data_recs = []
        result_recs = []
        for i in range(5):
            obj = Minimize(square(self.y_int - 0.2))
            p = Problem(obj, [self.A_bool == 0, self.x_bool == self.B_int])
            data_recs.append(p.get_problem_data(ECOS_BB))
            # result_recs.append( p.solve() )

        # Check that problem data and result is always the same.
        for i in range(1, 5):
            # self.assertEqual(result_recs[0], result_recs[i])
            for key in ["c", "A", "b", "G", "h",
                        "bool_vars_idx", "int_vars_idx"]:
                lh_item = data_recs[0][key]
                rh_item = data_recs[i][key]
                if key in ["A", "G"]:
                    lh_item = lh_item.todense()
                    rh_item = rh_item.todense()
                self.assertItemsAlmostEqual(lh_item, rh_item)

    def test_mip_print(self):
        """Test to string methods for Bool/Int vars.
        """
        self.assertEqual(repr(self.x_bool), "Bool(1, 1, 'x')")
        self.assertEqual(repr(self.B_int), "Int(2, 3, 'B')")

        x = Bool()
        B = Int(2, 3)

        self.assertEqual(repr(x), "Bool(1, 1)")
        self.assertEqual(repr(B), "Int(2, 3)")

    # def test_bool_prob(self):
    #     # Bool in objective.
    #     obj = Minimize(square(self.x_bool - 0.2))
    #     p = Problem(obj,[])
    #     result = p.solve()
    #     self.assertAlmostEqual(result, 0.04)

    #     self.assertAlmostEqual(self.x_bool.value, 0)

    #     # Bool in constraint.
    #     t = Variable()
    #     obj = Minimize(t)
    #     p = Problem(obj,[square(self.x_bool) <= t])
    #     result = p.solve()
    #     self.assertAlmostEqual(result, 0)

    #     self.assertAlmostEqual(self.x_bool.value, 0, places=4)

    #     # Matrix Bool in objective.
    #     C = matrix([[0, 1, 0], [1, 1, 1]])
    #     obj = Minimize(sum_squares(self.A_bool - C))
    #     p = Problem(obj,[])
    #     result = p.solve()
    #     self.assertAlmostEqual(result, 0)

    #     self.assertItemsAlmostEqual(self.A_bool.value, C, places=4)

    #     # Matrix Bool in constraint.
    #     t = Variable()
    #     obj = Minimize(t)
    #     p = Problem(obj, [sum_squares(self.A_bool - C) <= t])
    #     result = p.solve()
    #     self.assertAlmostEqual(result, 0)

    #     self.assertItemsAlmostEqual(self.A_bool.value, C, places=4)

    # def test_int_prob(self):
    #     # Int in objective.
    #     obj = Minimize(square(self.y_int - 0.2))
    #     p = Problem(obj,[])
    #     result = p.solve()
    #     self.assertAlmostEqual(result, 0.04)

    #     self.assertAlmostEqual(self.y_int.value, 0)
