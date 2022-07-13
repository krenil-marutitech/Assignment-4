import unittest
import requests

local_url = "http://127.0.0.1:9090"
access_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjU3NjkyMzAzLCJqdGkiOiI3MWY2OTI5ZS1hMWJlLTRhMTgtYmI1Yy04OWQxNjBlMWQxNGYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiODEzZTliYmU1NDViNDNkOGIyZDY0OTNiYjE4Zjk2MzYiLCJuYmYiOjE2NTc2OTIzMDMsImV4cCI6MTY1NzY5MzIwM30.RAkdGr47DODl4pkL2YSe2PtibmphdycHC1zH_Oyczc4'

search_message_response = {
    "messages": [
        "hello=world-3",
        "hello=world-4",
        "hello=world-1",
        "hello=world-2",
        "hello=world-3",
        "hello=world-4",
        "hello=world-3",
        "hello=world-4"
    ]
}

message_not_found = {
    "message": "Item not found."
}

search_by_category = {
    "Number of messages with category=direct": 7
}

category_not_found = {
    "message": "category not found."
}

body_search_by_date = {
    "date": "2022-07-08T17:35:38"
}

incorrect_time = {
    "date": "2022-07-08T17:37:38"
}

search_by_date = {
    "Number of messages with given Date/Time=2022-07-08T17:35:38": 2
}

date_not_found = {
    "message": "Data not found with given date."
}


class TestTrackerService(unittest.TestCase):
    def test_search_message(self):
        text = "he"
        res = requests.get(local_url + f"/api/search/{text}", headers={'Authorization': access_token})
        self.assertEqual(res.json(), search_message_response)
        self.assertEqual(res.status_code, 200)
        text_out = "helloUser"
        res = requests.get(local_url + f"/api/search/{text_out}", headers={'Authorization': access_token})
        self.assertEqual(res.json(), message_not_found)
        self.assertEqual(res.status_code, 404)

    def test_search_by_category(self):
        text = "direct"
        res = requests.get(local_url + f"/api/msg_count_by_category/{text}", headers={'Authorization': access_token})
        self.assertEqual(res.json(), search_by_category)
        self.assertEqual(res.status_code, 200)
        text_out = "proper"
        res = requests.get(local_url + f"/api/msg_count_by_category/{text_out}", headers={'Authorization': access_token})
        self.assertEqual(res.json(), category_not_found)
        self.assertEqual(res.status_code, 404)

    def test_search_by_date(self):
        res = requests.get(local_url + f"/api/msg_count_by_date", json=body_search_by_date, headers={'Authorization': access_token})
        self.assertEqual(res.json(), search_by_date)
        self.assertEqual(res.status_code, 200)
        res = requests.get(local_url + f"/api/msg_count_by_date", json=incorrect_time, headers={'Authorization': access_token})
        self.assertEqual(res.json(), date_not_found)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()