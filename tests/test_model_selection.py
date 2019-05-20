# -*- coding: utf-8 -*-

# LIBTwinSVM: A Library for Twin Support Vector Machines
# Developers: Mir, A.
# Version: 0.1 - 2019-03-20
# License: GNU General Public License v3.0

"""
This test module tests the functionalities of model_selection.py module
"""

from libtsvm.estimators import TSVM
from libtsvm.mc_scheme import OneVsAllClassifier
from libtsvm.model_selection import eval_metrics, search_space, get_results_filename, Validator
from libtsvm.preprocess import DataReader
import unittest
import numpy as np


class TestFunctions(unittest.TestCase):
    """
    It tests the functions of the model_selection.py module.
    """
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
    def test_eval_metrics(self):
        """
        It tests the evaluation metrics for binay estimators.
        """
        
        y_true = np.array([1, -1, 1, 1, -1])
        y_pred = np.array([1, 1, 1, 1, -1])
        
        expected_output = [3, 1, 1, 0, 80.0, 100.0, 75.0, 85.71, 50.0, 100.0,
                           66.67]
        
        tp, tn, fp, fn, acc, r_p, p_p, f1_p, r_n, p_n, f1_n = eval_metrics(y_true, y_pred)
        
        self.assertEqual([tp, tn, fp, fn, acc, r_p, p_p, float('%.2f' % f1_p),
                          r_n, p_n, float('%.2f' % f1_n)], expected_output)
        
    def test_search_space_linear(self):
        """
        It tests generated search space for linear kernel.
        """
        
        expected_output = [6, [{'C1': 0.5, 'C2': 1.0, 'gamma': 1},
                                {'C1': 0.5, 'C2': 2.0, 'gamma': 1},
                                {'C1': 1.0, 'C2': 1.0, 'gamma': 1},
                                {'C1': 1.0, 'C2': 2.0, 'gamma': 1},
                                {'C1': 2.0, 'C2': 1.0, 'gamma': 1},
                                {'C1': 2.0, 'C2': 2.0, 'gamma': 1}]]
        
        C1_range = (-1, 1)
        C2_range = (0, 1)
        u_range = None
        
        output = search_space('linear', 'full', C1_range, C2_range, u_range)
        
        self.assertEqual([len(output), output], expected_output)
        
    def test_search_space_rbf(self):
        """
        It tests generated search space for RBF kernel.
        """
        
        expected_output = [4, [{'C1': 2.0, 'C2': 0.125, 'gamma': 0.03125},
                           {'C1': 2.0, 'C2': 0.125, 'gamma': 0.0625},
                           {'C1': 2.0, 'C2': 0.25, 'gamma': 0.03125},
                           {'C1': 2.0, 'C2': 0.25, 'gamma': 0.0625}]]
        
        C1_range = (1, 1)
        C2_range = (-3, -2)
        u_range = (-5, -4)
        
        output = search_space('RBF', 'full', C1_range, C2_range, u_range)
        
        self.assertEqual([len(output), output], expected_output)
        
    def test_get_results_filename(self):
        """
        It tests filename of spreadsheet file.
        """
        
        f_name = 'Iris'
        clf_name = 'OVO-TSVM'
        ker_name = 'linear'
        test_method = ('CV', 10)
        
        ex_out_1 = "OVO-TSVM_linear_10-F-CV_Iris"
        
        out_1 = get_results_filename(f_name, clf_name, ker_name,
                                     test_method).split('_')
        
        test_method = ('t_t_split', 0.3)
        ex_out_2 = 'OVO-TSVM_linear_Tr70-Te30_Iris'
        
        out_2 = get_results_filename(f_name, clf_name, ker_name,
                                     test_method).split('_')
        
        print('_'.join(out_2[:len(out_2)-1]))
        self.assertEqual([ex_out_1, ex_out_2], ['_'.join(out_1[:len(out_1)-1]),
                         '_'.join(out_2[:len(out_2)-1])])
            
    def test_save_result(self):
        """
        It tests saving the classification results in a spreadsheet file.
        """
        
        # TODO: test should be implemented with a reliable assertion
        pass
        

class TestValidator(unittest.TestCase):
    """
    It tests the functionalities of Validator class.
    """
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.bin_clf = TSVM()
        self.mc_clf = OneVsAllClassifier(self.bin_clf)
        
        # Binary dataset
        bin_dataset = DataReader('./dataset/2d-synthetic.csv', ',', True)
        bin_dataset.load_data(False, False)
        self.bin_X, self.bin_y, _ = bin_dataset.get_data()
        
        # Multi-class data
        mc_dataset = DataReader('./dataset/mc-data.csv', ',', True)
        mc_dataset.load_data(False, False)
        self.mc_X, self.mc_y, _ = mc_dataset.get_data()
        
    def test_cv_validator(self):    
        """
        It tests cross-validation for a binary TSVM-based estimator.
        """
        
        expected_output = [100, 0.0]
        
        eval_m = Validator(self.bin_X, self.bin_y, ('CV', 5), self.bin_clf)
        eval_func = eval_m.choose_validator()
        acc, std, _ = eval_func({'C1': 1, 'C2': 1})
        
        self.assertEqual([acc, std], expected_output)
    
    def test_tt_validator(self):
        """
        It tests train/test split for a binary TSVM-based estimator.
        """
        
        expected_output = [100, 0.0]
        
        eval_m = Validator(self.bin_X, self.bin_y, ('t_t_split', 0.3),
                           self.bin_clf)
        eval_func = eval_m.choose_validator()
        acc, std, _ = eval_func({'C1': 1, 'C2': 1})
        
        self.assertEqual([acc, std], expected_output)
    
    def test_cv_validator_mc(self):
        """
        It tests cross-validation for a multi-class TSVM-based estimator.
        """
        
        expected_output = [100, 0.0]
        
        eval_m = Validator(self.mc_X, self.mc_y, ('CV', 5), self.mc_clf)  
        eval_func = eval_m.choose_validator()
        acc, std, _ = eval_func({'C1': 1, 'C2': 1})
        
        self.assertEqual([acc, std], expected_output)
    
    def test_tt_validator_mc(self):
        """
        It tests train/test split for a multi-class TSVM-based estimator.
        """
        
        expected_output = [100, 0.0]
        
        eval_m = Validator(self.mc_X, self.mc_y, ('t_t_split', 0.3),
                           self.mc_clf)
        eval_func = eval_m.choose_validator()
        acc, std, _ = eval_func({'C1': 1, 'C2': 1})
        
        self.assertEqual([acc, std], expected_output)
        
    def test_choose_validator(self):
        """
        It tests whether the right validator is returned.
        """
        
        output = []
        
        eval_m = Validator(self.bin_X, self.bin_y, ('CV', 5), self.bin_clf)
        
        output.append(eval_m.choose_validator().__name__ \
                      == Validator.cv_validator.__name__)
        
        eval_m = Validator(self.bin_X, self.bin_y, ('t_t_split', 0.3),
                           self.bin_clf)
        
        output.append(eval_m.choose_validator().__name__ \
                      == Validator.tt_validator.__name__)
        
        eval_m = Validator(self.mc_X, self.mc_y, ('CV', 5), self.mc_clf)
        
        output.append(eval_m.choose_validator().__name__ \
                      == Validator.cv_validator_mc.__name__)
        
        eval_m = Validator(self.mc_X, self.mc_y, ('t_t_split', 0.3),
                           self.mc_clf)
        
        output.append(eval_m.choose_validator().__name__ \
                      == Validator.tt_validator_mc.__name__)
        
        self.assertEqual(True, all(output))
        