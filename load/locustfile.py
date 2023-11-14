import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    x_auth_token = ""

    @task
    def view_items(self):
        self.client.headers = {
            "Content-Type": "application/json",
            "X-AUTH-TOKEN": self.x_auth_token
        }
        self.client.get(url="/v1/gooseAuth/items")
        time.sleep(1)

    def on_start(self):
        self.client.post(url="/v1/signUp",
                         json={
                             "userEmail": "test1@gmail.com",
                             "userPassword": "1q2w3e4r!@#",
                             "userNickname": "pepe"
                         })

        self.x_auth_token = self.client.post("/v1/signIn",
                                             json={
                                                 "userEmail": "test1@gmail.com",
                                                 "userPassword": "1q2w3e4r!@#",
                                             }).json()["data"]

        for name_index in range(10):
            self.client.headers = {
                "Content-Type": "application/json",
                "X-AUTH-TOKEN": self.x_auth_token
            }
            self.client.post(url="/v1/gooseAuth/addItems",
                             json={
                                 "name": f"{name_index}duck",
                                 "userName": "duck@goose.com",
                                 "userPassword": "Quarkquark12!",
                                 "folder": "goose",
                                 "notes": "I hate goose",
                                 "uri": [
                                     "https://www.youtube.com/watch?v=1P5yyeeYF9o",
                                     "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                                 ]
                             })
