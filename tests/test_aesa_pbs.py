import unittest.mock as mock

from aesa_pbs import add_aesa_pbs


@mock.patch("aesa_pbs.aesa_pbs.ExcelLCIAImporter")
@mock.patch("aesa_pbs.aesa_pbs.get_biosphere_database")
def test_add_aesa_pbs(mock_get_biosphere, mock_excel_importer):
    add_aesa_pbs(verbose=False)
    assert mock_get_biosphere.called
    assert mock_excel_importer.call_count > 0
