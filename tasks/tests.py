from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task

User = get_user_model()


class TaskAPISecurityTests(APITestCase):
    
    def setUp(self):
        # Create two independent users.
        self.user1 = User.objects.create_user(
            username = "user1",
            password="test-password-123"
        )
        
        self.user2 = User.objects.create_user(
            username="user2",
            password="test-password-456"
        )
        
        # Create one task for each user.
        self.task1 = Task.objects.create(
            title="User 1 task",
            description="Belongs to user 1",
            owner=self.user1
        )
        
        self.task2 = Task.objects.create(
            title = "User 2 task",
            description = "Belongs to user2",
            owner = self.user2
        )
        
        self.list_url = "/tasks/api/tasks/"
        self.detail_url = f"/tasks/api/tasks/{self.task2.id}/"
        
    def test_unauthenticated_user_cannot_list_tasks(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
    def test_user_only_sees_own_tasks(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        returned_ids = {
            task["id"] for task in response.data
        }
        
        self.assertIn(self.task1.id, returned_ids)
        self.assertNotIn(self.task2.id, returned_ids)
        
    def test_user_cannot_retrieve_another_users_task(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get(self.detail_url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        
        self.task2.refresh_from_db()
        
        self.assertFalse(self.task2.completed)
        
    def test_user_cannot_delete_another_users_task(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        
        self.assertTrue(
            Task.objects.filter(pk=self.task2.pk).exists()
        )
        
    def test_user_can_retrieve_own_task(self):
        self.client.force_authenticate(user=self.user2)
        
        response = self.client.get(
            f"/tasks/api/tasks/{self.task2.id}/"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], self.user2.id)
        
    def test_created_task_belongs_to_authenticated_user(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.post(
            self.list_url,
            {
                "title": "New test task",
                "description": "Created by automated test",
                "completed": False,
                "owner": self.user2.id,
            },
            format="json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
        created_task = Task.objects.get(pk=response.data["id"])
        
        self.assertEqual(created_task.owner, self.user1)
        
        
class TaskViewSetSecurityTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="viewset_user1",
            password="test-password-123"
        )

        self.user2 = User.objects.create_user(
            username="viewset_user2",
            password="test-password-456"
        )

        self.task1 = Task.objects.create(
            title="User 1 ViewSet task",
            description="Belongs to user 1",
            owner=self.user1
        )

        self.task2 = Task.objects.create(
            title="User 2 ViewSet task",
            description="Belongs to user 2",
            owner=self.user2
        )

        self.list_url = "/tasks/api/viewset/tasks/"
        self.task2_url = f"{self.list_url}{self.task2.id}/"

    def test_user_only_sees_own_tasks(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        returned_ids = {
            task["id"] for task in response.data["results"]
        }

        self.assertIn(self.task1.id, returned_ids)
        self.assertNotIn(self.task2.id, returned_ids)

    def test_user_cannot_retrieve_another_users_task(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.task2_url)

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_task(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.patch(
            self.task2_url,
            {"completed": True},
            format="json"
        )

        self.assertEqual(response.status_code, 404)

        self.task2.refresh_from_db()
        self.assertFalse(self.task2.completed)

    def test_user_cannot_delete_another_users_task(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(self.task2_url)

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Task.objects.filter(pk=self.task2.pk).exists()
        )

    def test_created_task_belongs_to_authenticated_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            self.list_url,
            {
                "title": "ViewSet created task",
                "description": "Ownership security test",
                "completed": False,
                "owner": self.user2.id,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        created_task = Task.objects.get(pk=response.data["id"])
        self.assertEqual(created_task.owner, self.user1)
    
    def test_unauthenticated_user_cannot_list_tasks(self):
        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ]
    )