const form = document.getElementById("taskForm");
const tbody = document.getElementById("taskTableBody");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const task = {
    title: document.getElementById("taskTitle").value,
    description: document.getElementById("taskDescription").value,
    due_date: document.getElementById("taskDueDate").value,
    priority: document.getElementById("taskPriority").value,
    status: "Pending"
  };

  fetch("/api/tasks/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Task Added:", data);
      loadTasks();
      form.reset();
    });
});

function loadTasks() {
  fetch("/api/tasks/")
    .then((res) => res.json())
    .then((data) => {
      tbody.innerHTML = "";
      data.forEach((task) => {
        tbody.innerHTML += `
          <tr>
            <td>${task.title}</td>
            <td>${task.description}</td>
            <td>${task.due_date || "-"}</td>
            <td>${task.priority || "-"}</td>
            <td>${task.status}</td>
            <td>
              <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">Delete</button>
            </td>
          </tr>
        `;
      });
    });
}

function deleteTask(id) {
  fetch(`/api/tasks/${id}`, { method: "DELETE" }).then(() => loadTasks());
}

// Load tasks on page load
loadTasks();
