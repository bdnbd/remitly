import unittest
from unittest.mock import patch, mock_open
from method import verify


class TestVerifyMethod(unittest.TestCase):

    def test_single_asterisk(self):
        json_data = '''
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "FirstStatement",
                    "Effect": "Allow",
                    "Action": ["iam:ChangePassword"],
                    "Resource": "*"
                }
            ]
        }
        '''
        with patch("builtins.open", mock_open(read_data=json_data)):
            result = verify("example.json")
            self.assertFalse(result)

    def test_without_single_asterisk(self):
        json_data = '''
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "arn:aws:s3:::confidential-data"
                    }
                ]
            }
        }

        '''
        with patch("builtins.open", mock_open(read_data=json_data)):
            result = verify("example.json")
            self.assertTrue(result)

    def test_invalid_json(self):
        with patch("builtins.open", mock_open(read_data="{")):
            result = verify("example.json")
            self.assertFalse(result)

    def test_missing_resource_field(self):
        json_data = '''
        {
        "PolicyName": "root",
        "PolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "IamListAccess",
                    "Effect": "Allow",
                    "Action": [
                        "iam:ListRoles",
                        "iam:ListUsers"
                    ],
                    "Resource": "arn:aws:s3:::confidential-data"
                }
            ]
        }
        }
        '''
        with patch("builtins.open", mock_open(read_data=json_data)):
            result = verify("example.json")
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
