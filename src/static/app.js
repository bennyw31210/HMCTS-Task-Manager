const apiUrl = 'http://localhost:8001/tasks';
const taskFormModal = document.getElementById('taskFormModal');
const createTaskBtn = document.getElementById('createTaskBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const taskForm = document.getElementById('taskForm');

// Fetch tasks from the backend
async function fetchTasks() {
    try {
        const response = await fetch(apiUrl);
        return await response.json();
    } catch (error) {
        alert('An error occurred while fetching tasks.');
        return [];
    }
}

// Update task due date colors based on their status
function updateTaskCards() {
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(taskCard => {
        const dueDate = new Date(taskCard.dataset.dueDate);
        const dueDateClass = getDueDateClass(dueDate);
        const dueDateElement = taskCard.querySelector('.due-date');

        dueDateElement.classList.remove('overdue', 'urgent', 'on-time');
        dueDateElement.classList.add(dueDateClass);

        const formattedDate = dueDate.toLocaleString();
        dueDateElement.innerHTML = `
            <span class="time-icon">⏰</span> ${formattedDate} 
            ${dueDateClass === 'overdue' ? '(Overdue)' : ''}
        `;
    });
}

// Set min date dynamically for the due date input
function setMinDueDate() {
    const minDate = new Date();
    minDate.setMinutes(minDate.getMinutes() + 1); // Add one minute to current time
    const formattedDate = minDate.toLocaleString('sv-SE').replace(' ', 'T').slice(0, 16); // Convert to yyyy-mm-ddThh:mm format
    document.getElementById('dueDate').setAttribute('min', formattedDate);
}

// Display task in the correct column based on status
function displayTask(task) {
    const taskCard = createTaskCard(task);
    const taskColumn = document.getElementById(`${task.status.toLowerCase().replace(' ', '-')}-list`);
    taskColumn.appendChild(taskCard);
}

// Create task card HTML element
function createTaskCard(task) {
    const taskCard = document.createElement('div');
    taskCard.classList.add('task-card');
    taskCard.id = `task-${task.id}`;
    taskCard.setAttribute('draggable', true);
    taskCard.dataset.dueDate = task.due_date;
    taskCard.ondragstart = (event) => onDragStart(event, task.id);

    const dueDate = new Date(task.due_date);
    const dueDateClass = getDueDateClass(dueDate);
    const formattedDate = dueDate.toLocaleString();

    taskCard.innerHTML = `
        <span class="delete-btn" onclick="deleteTask(${task.id})">
            <i class="fas fa-trash"></i>
        </span>
        <h3>${task.title}</h3>
        <p>${task.description}</p>
        <div class="due-date ${dueDateClass}">
            <span class="time-icon">⏰</span> ${formattedDate}
            ${dueDateClass === 'overdue' ? '(Overdue)' : ''}
        </div>
    `;

    return taskCard;
}

// Determine the background color based on due date
function getDueDateClass(dueDate) {
    const now = new Date();
    const diffInDays = (dueDate - now) / (1000 * 60 * 60 * 24);

    if (diffInDays < 0) return 'overdue';
    if (diffInDays < 1) return 'urgent';
    return 'on-time';
}

// Show toast notification
function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => toast.classList.remove('show'), 5000);
}

// Handle drag start
function onDragStart(event, taskId) {
    event.dataTransfer.setData('text', taskId);
}

// Allow drop into columns
function allowDrop(event) {
    event.preventDefault();
}

// Update task status when dropped into a new column
async function drop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('text');
    const task = await fetch(`${apiUrl}/${taskId}`);

    if (task.ok) {
        const taskData = await task.json();
        const newStatus = event.target.closest('.column').id.replace('-list', '').replace('pending', 'Pending').replace('in-progress', 'In Progress').replace('done', 'Done');
        
        const response = await fetch(`${apiUrl}/${taskId}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            taskData.status = newStatus;
            document.getElementById(`task-${taskId}`).remove();  // Remove the task from the current column
            displayTask(taskData);  // Add it to the new column
        } else {
            alert('Error updating task status');
        }
    }
}

// Delete task
async function deleteTask(taskId) {
    const confirmed = confirm('Are you sure you want to delete this task?');
    if (confirmed) {
        const response = await fetch(`${apiUrl}/${taskId}/`, { method: 'DELETE' });

        if (response.ok) {
            showToast('Task deleted successfully!');
            document.getElementById(`task-${taskId}`).remove();
        } else {
            alert('Error deleting task');
        }
    }
}

// Open the create task modal
createTaskBtn.addEventListener('click', () => taskFormModal.style.display = 'block');

// Close the modal
closeModalBtn.addEventListener('click', closeCreateTaskForm);
cancelBtn.addEventListener('click', closeCreateTaskForm);

// Clear the form and close the modal
function closeCreateTaskForm() {
    taskFormModal.style.display = 'none';
    taskForm.reset();
}

// Handle form submission to create a new task
taskForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const status = document.getElementById('status').value;
    const dueDate = document.getElementById('dueDate').value;

    const newTask = { title, description, status, due_date: new Date(dueDate).toISOString() };

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
    });

    if (response.ok) {
        const task = await response.json();
        displayTask(task);
        closeCreateTaskForm();
        showToast('Task created successfully!');
    } else {
        alert('Error creating task');
    }
});

// Ensure state updates to time related elements are carried out exactly on the minute every minute
function startMinuteUpdates() {
    const now = new Date();
    const msUntilNextMinute = 60000 - (now.getSeconds() * 1000 + now.getMilliseconds());

    // Wait until the start of the next full minute
    setTimeout(() => {
        updateTaskCards();
        setMinDueDate();

        // Then repeat every full minute
        setInterval(() => {
            updateTaskCards();
            setMinDueDate();
        }, 60000);
    }, msUntilNextMinute);
}

// Run when the page loads
window.onload = async () => {
    const tasks = await fetchTasks();  // Fetch tasks from the backend
    tasks.forEach(task => displayTask(task));  // Display each task
    setMinDueDate();    // Set minimum due date that can be assigned to a new task
    startMinuteUpdates();   // Carry out subsequent state updates for time-reliant elements on the minute every minute
};