import { sendForm } from "./request.js";

// purpose of Notes is to activate the creation form
export class Notes {
  constructor() {
    this.allNoteLists = document.querySelectorAll(".note-list");
    this.allNotes = document.querySelectorAll(".note-card");
    // activating the creation form
    this.activateAllCreateForms();
  }

  /*
    looping through all the note lists
    for each note list that you find, you’re selecting the .person-card element that the note list is in
    and getting the corresponding personID
  */
  activateAllCreateForms() {
    this.allNoteLists.forEach((noteList) => {
      const personCard = noteList.closest(".person-card");
      const personID = personCard.getAttribute("data-person-id");
      new NoteCreateForm(noteList, personID);
    });
  }
}

export class NoteCreateForm {
  constructor(noteList, personID) {
    this.noteList = noteList;
    this.personID = personID;
    this.form = this.noteList.querySelector(".note-create-card form");
    this.createButton = this.form.querySelector(
      "button[data-action='create']"
    );
    // connecting createButton to .handleCreateClick()
    this.createButton.addEventListener(
      "click",
      this.handleCreateClick.bind(this)
    );
    // you call .connectPerson() to make sure that the ID of the creation form matches the targeted person
    this.connectPerson();
  }

  connectPerson() {
    let fieldPersonID = this.form.querySelector("input[name='person_id']");
    fieldPersonID.setAttribute("value", this.personID);
  }

  handleCreateClick(event) {
    event.preventDefault();
    // when you click the Create button, then you make a POST request to the API
    sendForm(this.form, "POST", "/api/notes", this.addNoteToList);
    // if the API request is done, then you clear the form input fields with .reset()
    this.form.reset();
  }

  addNoteToList(rawData) {
    const data = JSON.parse(rawData);
    const noteList = document
      .querySelector("[data-person-id= '" + data.person_id + "']")
      .querySelector(".note-list");
    // when .addNoteToList() executes, then you select the first .note-card of your document
    const newNoteCard = document.querySelector(".note-card").cloneNode(true);
    // This is the note card of another person. That’s why you need to adjust its contents and attributes after cloning it
    newNoteCard.querySelector(".note-content").textContent = data.content;
    newNoteCard.setAttribute("data-note-id", data.id);
    // add noteCard to noteList
    noteList.insertBefore(newNoteCard, noteList.children[1]);
  }
}