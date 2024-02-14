import numpy as np
from locust import HttpUser, between, task

movie_reviews =  [
    "Scientists Discover New Species in Amazon Rainforest",
    "Breakthrough in Cancer Research Offers Hope for Patients",
    "Global Leaders Unveil Plan for Sustainable Energy Future",
    "Artificial Intelligence Revolutionizing Healthcare Diagnostics",
    "Mars Rover Sends Stunning Images of Martian Landscape",
    "World-renowned Chef Opens Innovative Plant-Based Restaurant",
    "International Space Station Celebrates 25 Years in Orbit",
    "Groundbreaking Study Reveals Secrets of Longevity",
    "Major Tech Company Launches Cutting-edge Augmented Reality Device",
    "Humanitarian Aid Reaches Remote Areas Amidst Global Crisis"
]


class PredictUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict(self):
        num_of_review = np.random.randint(1, 100)
        reviews = np.random.choice(movie_reviews, size=num_of_review, replace=True)
        self.client.post("/predict", json={"text": reviews.tolist()})
