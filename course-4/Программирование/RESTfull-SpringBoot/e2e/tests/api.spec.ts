import { test, expect } from '@playwright/test';

test.describe('Task Management System API', () => {
  const baseURL = 'http://localhost:8080/api/tasks';
  const auth = {
    username: 'admin',
    password: 'admin123'
  };
  const headers = {
    'Authorization': 'Basic ' + Buffer.from(`${auth.username}:${auth.password}`).toString('base64'),
    'Content-Type': 'application/json'
  };

  test('CRUD Operations', async ({ request }) => {
    // 1. Create a new task
    const newTask = {
      title: 'Playwright Task',
      description: 'Task created by Playwright',
      status: 'Pending'
    };

    const createResponse = await request.post(baseURL, {
      headers: headers,
      data: newTask
    });
    expect(createResponse.status()).toBe(200);
    const createdTask = await createResponse.json();
    console.log('Created Task:', createdTask);
    expect(createdTask.title).toBe(newTask.title);

    // 2. Get all tasks
    const listResponse = await request.get(baseURL, {
      headers: headers
    });
    expect(listResponse.status()).toBe(200);
    const tasks = await listResponse.json();
    console.log('All Tasks:', tasks);
    expect(tasks.length).toBeGreaterThan(0);

    // 3. Update the task
    const updatedTaskData = {
      title: 'Playwright Task Updated',
      description: 'Updated description',
      status: 'In Progress'
    };
    const updateResponse = await request.put(`${baseURL}/${createdTask.id}`, {
      headers: headers,
      data: updatedTaskData
    });
    expect(updateResponse.status()).toBe(200);
    const updatedTask = await updateResponse.json();
    console.log('Updated Task:', updatedTask);
    expect(updatedTask.status).toBe('In Progress');

    // 4. Delete the task
    const deleteResponse = await request.delete(`${baseURL}/${createdTask.id}`, {
      headers: headers
    });
    expect(deleteResponse.status()).toBe(200);

    // 5. Verify deletion
    const getResponse = await request.get(`${baseURL}/${createdTask.id}`, {
      headers: headers
    });
    expect(getResponse.status()).toBe(404);
  });
});
