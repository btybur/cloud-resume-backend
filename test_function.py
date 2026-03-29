import unittest
from unittest.mock import MagicMock, patch
import azure.functions as func
from function_app import visitorcounter

class TestVisitorCounter(unittest.TestCase):

    @patch.dict('os.environ', {'COSMOS_CONNECTION_STRING': 'fake_connection_string'})
    @patch('function_app.TableServiceClient')
    def test_existing_counter_increments(self, mock_table_service):
        mock_entity = {"count": 5, "PartitionKey": "counter", "RowKey": "visits"}
        mock_table_client = MagicMock()
        mock_table_client.get_entity.return_value = mock_entity
        mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table_client

        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/visitorcounter',
            params={}
        )

        response = visitorcounter(req)
        self.assertEqual(response.status_code, 200)
        self.assertIn('6', response.get_body().decode())

    @patch.dict('os.environ', {'COSMOS_CONNECTION_STRING': 'fake_connection_string'})
    @patch('function_app.TableServiceClient')
    def test_new_counter_starts_at_one(self, mock_table_service):
        mock_table_client = MagicMock()
        mock_table_client.get_entity.side_effect = Exception("Entity not found")
        mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table_client

        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/visitorcounter',
            params={}
        )

        response = visitorcounter(req)
        self.assertEqual(response.status_code, 200)
        self.assertIn('1', response.get_body().decode())

    @patch.dict('os.environ', {'COSMOS_CONNECTION_STRING': 'fake_connection_string'})
    @patch('function_app.TableServiceClient')
    def test_response_is_valid_json(self, mock_table_service):
        mock_entity = {"count": 3, "PartitionKey": "counter", "RowKey": "visits"}
        mock_table_client = MagicMock()
        mock_table_client.get_entity.return_value = mock_entity
        mock_table_service.from_connection_string.return_value.get_table_client.return_value = mock_table_client

        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/visitorcounter',
            params={}
        )

        response = visitorcounter(req)
        import json
        body = json.loads(response.get_body().decode())
        self.assertIn('count', body)

if __name__ == '__main__':
    unittest.main()