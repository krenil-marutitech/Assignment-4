import unittest
import requests

local_url = "http://127.0.0.1:9092"
access_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjU3NjkyMzAzLCJqdGkiOiI3MWY2OTI5ZS1hMWJlLTRhMTgtYmI1Yy04OWQxNjBlMWQxNGYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiODEzZTliYmU1NDViNDNkOGIyZDY0OTNiYjE4Zjk2MzYiLCJuYmYiOjE2NTc2OTIzMDMsImV4cCI6MTY1NzY5MzIwM30.RAkdGr47DODl4pkL2YSe2PtibmphdycHC1zH_Oyczc4'

add_new_messages = [
    {
        "user_message": "Hello there!"
    },
    {
        "user_message": "How are you?"
    }
]

response_message = {
    "message": "Messages are sent."
}


class TestDataPusherService(unittest.TestCase):
    def test_add_new_messages(self):
        # add new messages
        res = requests.get(local_url + "/api/send_message", json=add_new_messages, headers={'Authorization': access_token})
        self.assertEqual(res.json(), response_message)
        self.assertEqual(res.status_code, 201)


if __name__ == "__main__":
    unittest.main()
