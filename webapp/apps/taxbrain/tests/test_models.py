from django.test import TestCase
import pytest

from ..models import JSONReformTaxCalculator, TaxSaveInputs
from ..forms import TaxBrainForm
from ...test_assets.utils import get_taxbrain_model, stringify_fields
from ...test_assets.test_models import TaxBrainTableResults, TaxBrainFieldsTest


class TaxBrainJSONReformModelTest(TestCase):
    """Test taxbrain JSONReformTaxCalculator."""

    def setUp(self):
        # Every test needs a client.
        self.test_string = "".join(["1" for x in range(100000)])

    def test_create_reforms(self):
        self.reforms = JSONReformTaxCalculator.objects.create(
            reform_text=self.test_string,
            raw_reform_text=self.test_string,
            assumption_text=self.test_string,
            raw_assumption_text=self.test_string
        )


class TaxBrainStaticResultsTest(TaxBrainTableResults, TestCase):

    def test_static_tc_lt_0130(self):
        self.tc_lt_0130(self.test_coverage_fields)

    def test_static_tc_gt_0130(self):
        self.tc_gt_0130(self.test_coverage_fields)


class TaxBrainStaticFieldsTest(TaxBrainFieldsTest, TestCase):

    def test_set_fields(self):
        start_year = 2017
        fields = self.test_coverage_gui_fields.copy()
        fields['first_year'] = start_year

        self.parse_fields(start_year, fields, Form=TaxBrainForm)

    def test_old_runs(self):
        """
        Test that the fields JSON objects can be generated dyanamically
        """
        start_year = 2017
        tsi = TaxSaveInputs(
            ID_AmountCap_Switch_0='True',
            FICA_ss_trt='0.10',
            STD_cpi='True',
            first_year=start_year
        )
        tsi.save()
        tsi.set_fields()
        assert tsi.input_fields['_FICA_ss_trt'] == [0.10]
        assert tsi.input_fields['_STD_cpi'] == True
        assert tsi.input_fields['_ID_AmountCap_Switch_medical'] == [True]

    def test_deprecated_fields(self):
        """
        Test that deprecated fields are added correctly
        """
        return
        start_year = 2017
        tsi = TaxSaveInputs(
            raw_input_fields = {
                'FICA_ss_trt': '0.10',
                'ID_BenefitSurtax_Switch_0': 'True',
                'STD_cpi': 'True',
                'deprecated_param': '1000'
            },
            first_year=start_year
        )
        tsi.set_fields()
        assert tsi.deprecated_fields == ['deprecated_param']
        tsi.raw_input_fields['yet_another_deprecated_param'] = '1001'
        tsi.set_fields()
        assert tsi.deprecated_param == ['deprecated_param',
                                        'yet_another_deprecated_param']
        assert tsi.raw_input_fields['deprecated_param'] == '1000'
        assert tsi.raw_input_fields['yet_another_deprecated_param'] == '1001'
        assert 'deprecated_param' not in tsi.input_fields
        assert 'yet_another_deprecated_param' not in tsi.input_fields
