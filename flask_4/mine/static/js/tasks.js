
import { sendForm } from "./request.js";

export class Tasks {
  constructor() {
    this.allTaskLists = document.querySelectorAll(".task-list");
    this.allTasks = document.querySelectorAll(".task-card");
    this.activateAllCreateForms();
  }

  activateAllCreateForms() {
    this.allTaskLists.forEach((taskList) => {
      const personCard = taskList.closest(".person-card");
      const personID = personCard.getAttribute("data-person-id");
      new TaskCreateForm(taskList, personID);
    });
  }
}

export class TaskCreateForm {
  constructor(taskList, personID) {
    this.taskList = taskList;
    this.personID = personID;
    this.form = this.taskList.querySelector(".task-create-card form");
    this.createButton = this.form.querySelector(
      "button[data-action='create']"
    );
    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
    this.connectPerson();
  }

  connectPerson() {
    let fieldPersonID = this.form.querySelector("input[name='person_id']");
    fieldPersonID.setAttribute("value", this.personID);
  }

  handleCreateClick(event) {
    event.preventDefault();
    sendForm(this.form, "POST", "/api/tasks", this.addTaskToList);
    this.form.reset();
  }

  addTaskToList(rawData) {
    const data = JSON.parse(rawData);
    const taskList = document
      .querySelector("[data-person-id= '" + data.person_id + "']")
      .querySelector(".task-list");
    

    const newTaskCard = document.querySelector(".task-card").cloneNode(true);
    
    newTaskCard.querySelector(".task-name").textContent = data.name;
    newTaskCard.setAttribute("data-task-id", data.id);
    
    taskList.insertBefore(newTaskCard, taskList.children[1]);

    /*
    newTaskCard
      .querySelectorAll(".comme-card")
      .forEach((noteCard) => noteCard.remove());*/
    new TaskControl(personCard);
  }
}

class TaskControl {
  constructor(taskCard) {
    this.taskCard = taskCard;
    this.taskElement = this.taskCard.querySelector(".task-content");
    this.taskControl = this.taskCard.querySelector(".task-control");
    this.taskID = this.taskCard.getAttribute("data-task-id");
    this.form = this.taskCard.querySelector("form");

    this.editBtn = this.taskCard.querySelector(".toggle-control");
    this.editBtn.addEventListener("click", this.handleEditClick.bind(this));
    this.cancelBtn = this.taskCard.querySelector("[data-action='cancel']");
    this.cancelBtn.addEventListener(
      "click",
      this.handleCancelClick.bind(this)
    );
    this.deleteBtn = this.taskCard.querySelector("[data-action='delete']");
    this.deleteBtn.addEventListener(
      "click",
      this.handleDeleteClick.bind(this)
    );
    this.updateBtn = this.taskCard.querySelector("[data-action='update']");
    this.updateBtn.addEventListener(
      "click",
      this.handleUpdateClick.bind(this)
    );

    this.fillControlForm();
  }

  handleEditClick(event) {
    event.preventDefault();
    this.taskCard
      .querySelector(".task-control-card")
      .classList.add("editing");
    this.taskElement.classList.add("hidden");
    this.editBtn.classList.add("hidden");
    this.taskControl.classList.remove("hidden");
  }

  handleCancelClick(event) {
    event.preventDefault();
    this.taskCard
      .querySelector(".task-control-card")
      .classList.remove("editing");
    this.taskElement.classList.remove("hidden");
    this.editBtn.classList.remove("hidden");
    this.taskControl.classList.add("hidden");
  }

  handleDeleteClick(event) {
    event.preventDefault();
    const endpoint = "/api/tasks/" + this.taskID;
    sendForm(this.form, "DELETE", endpoint, (data, inputForm) => {
      let taskCard = inputForm.closest(".task-card");
      if (window.confirm("Do you really want to remove this task?")) {
        taskCard.remove();
      }
    });
  }

  handleUpdateClick(event) {
    event.preventDefault();
    const endpoint = "/api/tasks/" + this.taskID;
    sendForm(this.form, "PUT", endpoint, this.updateTaskInList);
    this.cancelBtn.click();
  }

  updateTaskInList(rawData, inputForm) {
    const data = JSON.parse(rawData);
    const taskCard = inputForm.closest(".task-card");

    const taskFirstName = taskCard.querySelector("[data-task-name]");
    taskFirstName.textContent = data.name;
    taskFirstName.setAttribute("data-task-name", data.name);

    const taskLastName = taskCard.querySelector("[data-task-date]");
    taskLastName.textContent = data.date;
    taskLastName.setAttribute("data-task-date", data.date);
  }

  fillControlForm() {
    const taskFirstName = this.taskElement.querySelector(
      "[data-task-name]"
    ).textContent;
    const taskLastName = this.taskElement.querySelector(
      "[data-task-date]"
    ).textContent;
    this.form
      .querySelector("[name='id']")
      .setAttribute("value", this.taskID);
    this.form
      .querySelector("[name='name']")
      .setAttribute("value", taskFirstName);
    this.form
      .querySelector("[name='date']")
      .setAttribute("value", taskLastName);
  }
}