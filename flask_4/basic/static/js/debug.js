import { getData } from "./request.js";

/*
  adding functionality to your form inside of the .debug-card element
  (here) the DebugForm class controls the debug <div> element
*/
export class DebugForm {
  constructor() {
    this.debugCard = document.querySelector(".debug-card");
    this.form = this.debugCard.querySelector(".debug-form");

    /*
    note the call to .bind() when referencing the event handler handleClearClick() in the .addEventListener() method
    this allows the event handler to call the this keyword as if it were an instance of the DebugForm
    binding allows the handler to have access to all the properties defined in the constructor, like this.debugCard
    */
    this.clearButton = this.form.querySelector("button[data-action='clear']");
    this.clearButton.addEventListener(
      "click",
      this.handleClearClick.bind(this)
    );

    this.sendButton = this.form.querySelector("button[data-action='read']");
    this.sendButton.addEventListener("click", this.handleSendClick.bind(this));
  }

  handleClearClick(event) {
    event.preventDefault();
    let code = this.debugCard.querySelector("code");
    code.innerText = "";
  }

  handleSendClick(event) {
    event.preventDefault();
    const input = document.querySelector(".debug-card input");
    const endpoint = input.value;
    getData(endpoint, this.showResponse);
  }

  /*
  .showResponse() as a callback function that’s executed once getData() runs successfully
  instead of clearing the content of your <code> element like you do in .handleClearClick(),
  you’re showing the data that .showResponse() receives
  */
  showResponse(data) {
    const debugCard = document.querySelector(".debug-card");
    let code = debugCard.querySelector("code");
    code.innerText = data;
  }
}