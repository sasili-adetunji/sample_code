import base64
import json
import sys
from unittest import mock, TestCase, main
from io import StringIO

from app import create_app
from nest import read_input, missing_levels, parse_json

test = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100
    },
    {
        "country": "FR",
        "city": "Paris",
        "currency": "EUR",
        "amount": 20
    },
    {
        "country": "FR",
        "city": "Lyon",
        "currency": "EUR",
        "amount": 11.4
    },
    {
        "country": "ES",
        "city": "Madrid",
        "currency": "EUR",
        "amount": 8.9
    },
    {
        "country": "UK",
        "city": "London",
        "currency": "GBP",
        "amount": 12.2
    },
    {
        "country": "UK",
        "city": "London",
        "currency": "FBP",
        "amount": 10.9
    }
    ]

class ParseJsonTestCase(TestCase):

    def setUp(self):
        self.test_data = [
            {
                "country": "US",
                "city": "Boston",
                "currency": "USD",
                "amount": 100
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            },
            {
                "country": "FR",
                "city": "Lyon",
                "currency": "EUR",
                "amount": 11.4
            },
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 8.9
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "GBP",
                "amount": 12.2
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "FBP",
                "amount": 10.9
            }
        ]

    @mock.patch("sys.stdin", StringIO(json.dumps(test)))
    def test_read_input_from_stdin(self):

        test_input = [
            {
                "country": "US",
                "city": "Boston",
                "currency": "USD",
                "amount": 100
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            },
            {
                "country": "FR",
                "city": "Lyon",
                "currency": "EUR",
                "amount": 11.4
            },
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 8.9
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "GBP",
                "amount": 12.2
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "FBP",
                "amount": 10.9
            }
        ]

        self.assertEqual(read_input(), test_input)

    def test_missing_levels(self):
        nlevels = ['currency', 'country']
        data =  {
            'country': 'US',
            'city': 'London',
            'currency': 'GPB',
            'amount': 12
        }
        result = missing_levels(nlevels, data)
        expected_result = [{'city': 'London'}, {'amount': 12}]
        self.assertEqual(result, expected_result)

    def test_parse_json(self):

        nlevels = ['currency', 'country']

        result = parse_json(self.test_data, nlevels)
        expected_result = {'USD': {'US': [{'city': 'Boston'}, {'amount': 100}]}, 'EUR': {'FR': [{'city': 'Lyon'}, {'amount': 11.4}], 'ES': [{'city': 'Madrid'}, {'amount': 8.9}]}, 'GBP': {'UK': [{'city': 'London'}, {'amount': 12.2}]}, 'FBP': {'UK': [{'city': 'London'}, {'amount': 10.9}]}}
        self.assertEqual(result, expected_result)

    def test_parse_json_with_case_sensitive_nlevels(self):

        nlevels = ['Currency', 'Country']
        result = parse_json(self.test_data, nlevels)
        expected_result = {'USD': {'US': [{'city': 'Boston'}, {'amount': 100}]}, 'EUR': {'FR': [{'city': 'Lyon'}, {'amount': 11.4}], 'ES': [{'city': 'Madrid'}, {'amount': 8.9}]}, 'GBP': {'UK': [{'city': 'London'}, {'amount': 12.2}]}, 'FBP': {'UK': [{'city': 'London'}, {'amount': 10.9}]}}
        self.assertEqual(result, expected_result)

    def test_parse_json_with_nlevels_not_in_keys(self):

        nlevels = ['Curr', 'Country']
        result = parse_json(self.test_data, nlevels)
        self.assertFalse(result)


class ParseJsonApiTestCase(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_data = [
            {
                "country": "US",
                "city": "Boston",
                "currency": "USD",
                "amount": 100
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            },
            {
                "country": "FR",
                "city": "Lyon",
                "currency": "EUR",
                "amount": 11.4
            },
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 8.9
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "GBP",
                "amount": 12.2
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "FBP",
                "amount": 10.9
            }
        ]
        self.expected_result = {
            "USD": {
                "US": {
                    "Boston": [
                        {
                            "amount": 100
                        }
                    ]
                }
            },
            "EUR": {
                "FR": {
                    "Paris": [
                        {
                            "amount": 20
                        }
                    ],
                    "Lyon": [
                        {
                            "amount": 11.4
                        }
                    ]
                },
                "ES": {
                    "Madrid": [
                        {
                            "amount": 8.9
                        }
                    ]
                }
            },
            "GBP": {
                "UK": {
                    "London": [
                        {
                            "amount": 12.2
                        }
                    ]
                }
            },
            "FBP": {
                "UK": {
                    "London": [
                        {
                            "amount": 10.9
                        }
                    ]
                }
            }
        }
        self.valid_credentials = base64.b64encode(b'testUser:SuperSecretP@ssw0rd!').decode('utf-8')

    def test_parse_json_api_without_auth(self):
        res = self.client.post(
            '/api?nlevels=currency,country,city',
            data=json.dumps(self.test_data),
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual('Please authenticate to access this API.', data['message'])

    def test_parse_json_api_with_wrong_auth(self):

        self.valid_credentials = base64.b64encode(b'anotherUser:Another@ssw0rd!').decode('utf-8')

        res = self.client.post(
            '/api?nlevels=currency,country,city',
            data=json.dumps(self.test_data),
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual('Please authenticate to access this API.', data['message'])

    def test_parse_json_api_returns_ok(self):

        res = self.client.post(
            '/api?nlevels=currency,country,city',
            data=json.dumps(self.test_data),
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(self.expected_result, data['data'])

    def test_parse_json_api_without_nlevels_params(self):
        res = self.client.post(
            '/api',
            data=json.dumps(self.test_data),
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Please provide nlevels as parameters")

    def test_parse_json_api_with_wrong_nlevels_params(self):
        res = self.client.post(
            '/api?nlevels=currency,country,city,something',
            data=json.dumps(self.test_data),
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "nlevels must be one of the keys in the json array")

if __name__ == '__main__':
    main()
