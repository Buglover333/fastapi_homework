# tests/test_task_service.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from schemas.task import Task

class TestTaskService:
    def test_create_task(self):
        mock_repo = Mock()
        mock_task = Task(task_id=1, task_text="Test task", task_deadline=datetime.now())
        mock_repo.create.return_value = mock_task
        
        with patch('api.routers.taskmanager.tasks', []):
            with patch('api.routers.taskmanager.counter', 0):
                from api.routers.taskmanager import create_task
                
                result = create_task(task_text="Test task")
                
                assert result.task_id == 1
                assert result.task_text == "Test task"