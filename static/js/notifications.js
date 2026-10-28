const websocketUrl = JSON.parse(
    document.getElementById("websocket-url").textContent
);
const socket = new WebSocket(websocketUrl);

socket.onopen = function () {
    console.log("Connected to WebSocket server");
};

socket.onmessage = function (event) {
    const notification = JSON.parse(event.data);

    console.log("New notification:", notification);

    if(notification.type === "connection_established") return;

    showNotificationToast(notification);
};

socket.onclose = function () {
    console.log("WebSocket connection closed");
};

socket.onerror = function (error) {
    console.error("WebSocket error:", error);
};

const toastContainer = document.getElementById(
    "notification-toast-container"
);

const notificationTypes = {
    "project.update": {
        title: "Project Updated",
        icon: "bi-folder2-open",
    },
    "project.join_request": {
        title: "New Join Request",
        icon: "bi-person-plus",
    },
    "project.join_response": {
        title: "Join Request Responded",
        icon: "bi-person-check",
    },
    "task.add": {
        title: "New Task",
        icon: "bi-plus-square",
    },
    "task.update": {
        title: "Task Updated",
        icon: "bi-pencil-square",
    },
    "task.assignee.add": {
        title: "Task Assignees Updated",
        icon: "bi-people",
    },
    "task.assignee.remove": {
        title: "Task Assignees Updated",
        icon: "bi-people",
    },
    "task.comment.add": {
        title: "New Task Comment",
        icon: "bi-chat-left-text",
    },
};

function getNotificationTitle(notification) {
    return notificationTypes[notification.event_type]?.title
        ?? "Notification";
}

function getNotificationIcon(notification) {
    return notificationTypes[notification.event_type]?.icon
        ?? "bi-bell";
}

function getNotificationMessage(notification) {
    const payload = notification.payload ?? {};

    switch (notification.event_type) {
        case "project.update": {
            const projectTitle =
                payload.title?.new ||
                payload.title?.old ||
                "Project";

            const details = [];

            if (
                payload.title &&
                payload.title.old !== payload.title.new
            ) {
                details.push(
                    `Title changed from "${payload.title.old}" to "${payload.title.new}".`
                );
            }

            if (
                payload.description &&
                payload.description.old !== payload.description.new
            ) {
                details.push("Project description was updated.");
            }

            if (
                payload.topics &&
                payload.topics.old !== payload.topics.new
            ) {
                details.push("Project topics were updated.");
            }

            return `The project "${projectTitle}" has been updated.` +
                (details.length ? "\n" + details.join("\n") : "");
        }

        case "project.join_request":
            return `A new join request has been submitted for the project "${payload.project_title || "Project"}".`;

        case "project.join_response": {
            const status = payload.join_status;

            if (status === "ACC") {
                return `Your join request for the project "${payload.project_title || "Project"}" has been approved.`;
            }

            if (status === "REJ") {
                return `Your join request for the project "${payload.project_title || "Project"}" has been rejected.`;
            }

            return `Your join request for the project "${payload.project_title || "Project"}" has been updated.`;
        }

        case "task.add":
            return `A new task, "${payload.task_title || "Task"}", has been added to your project.`;

        case "task.update": {
            const taskTitle =
                payload.title?.new ||
                payload.task_title ||
                payload.title?.old ||
                "Task";

            const details = [];

            if (
                payload.title &&
                payload.title.old !== payload.title.new
            ) {
                details.push(
                    `Title changed from "${payload.title.old}" to "${payload.title.new}".`
                );
            }

            if (
                payload.description &&
                payload.description.old !== payload.description.new
            ) {
                details.push("Task description was updated.");
            }

            if (
                payload.status &&
                payload.status.old !== payload.status.new
            ) {
                details.push(
                    `Status changed from "${payload.status.old}" to "${payload.status.new}".`
                );
            }

            return `The task "${taskTitle}" has been updated.` +
                (details.length ? "\n" + details.join("\n") : "");
        }

        case "task.assignee.add":
            return `Assignees have been added to the task "${payload.task_title || "Task"}".`;

        case "task.assignee.remove":
            return `Assignees have been removed from the task "${payload.task_title || "Task"}".`;

        case "task.comment.add":
            return `A new comment has been added to the task "${payload.task_title || "Task"}".`;

        default:
            return "You have a new notification.";
    }
}

function showNotificationToast(notification) {
    if (!toastContainer) {
        return;
    }

    const toastTitle = getNotificationTitle(notification);
    const toastIcon = getNotificationIcon(notification);
    const toastMessage = getNotificationMessage(notification);

    // Create elements safely; do not inject notification data as HTML.
    const toastElement = document.createElement("div");
    toastElement.className = "toast border-0 shadow-sm mb-2";
    toastElement.setAttribute("role", "status");
    toastElement.setAttribute("aria-atomic", "true");

    const toastHeader = document.createElement("div");
    toastHeader.className = "toast-header";

    const icon = document.createElement("i");
    icon.className = `bi ${toastIcon} fs-5 me-2`;
    icon.setAttribute("aria-hidden", "true");

    const title = document.createElement("strong");
    title.className = "me-auto";
    title.textContent = toastTitle;

    const timestamp = document.createElement("small");
    timestamp.className = "text-body-secondary";
    timestamp.textContent = "Just now";

    const closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className = "btn-close";
    closeButton.setAttribute("data-bs-dismiss", "toast");
    closeButton.setAttribute("aria-label", "Close");

    toastHeader.append(icon, title, timestamp, closeButton);

    const toastBody = document.createElement("div");
    toastBody.className = "toast-body";
    toastBody.style.whiteSpace = "pre-line";
    toastBody.textContent = toastMessage;

    toastElement.append(toastHeader, toastBody);
    toastContainer.appendChild(toastElement);

    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 6000,
    });

    toastElement.addEventListener("hidden.bs.toast", function () {
        toastElement.remove();
    });

    toast.show();
}