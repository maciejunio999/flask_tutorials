
/* 
  # export declaration ('export' before 'function') makes values available
    in other JavaScriot modules
  # with getData(), you’re introducing the first Ajax function to your
    Flask project. Ajax stands for Asynchronous JavaScript and XML
*/
export function getData(endpoint, callback) {
    // creat a new XMLHttpRequest object that you use to make requests
    const request = new XMLHttpRequest();
    // binds the .onreadystatechange() event to request. It triggers when you change .readyState() by sending the request in line 14
    request.onreadystatechange = () => {
      // value 4 indicates the DONE state
      if (request.readyState === 4) {
        // calls the provided callback function with request.response when the request operation is complete
        callback(request.response);
      }
    };
    // initializes your request with a GET HTTP action and the provided endpoint URL
    request.open("GET", endpoint);
    // ends the request and triggers .onreadystatechange() when done
    request.send();
}
/*
  in short, function above makes a GET HTTP request with your API when you call getData(), as you do in DebugForm.onSendClick()
*/



export function sendForm(form, action, endpoint, callback) {
  // create a JSON object by serializing your form data
    const formData = new FormData(form);
    const dataJSON = JSON.stringify(Object.fromEntries(formData));
  
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {
      if (request.readyState === 4) {
        callback(request.response, form);
      }
    };
    request.open(action, endpoint);
    // set the request’s content type to JSON
    request.setRequestHeader("Content-Type", "application/json");
    // set the request’s content type to JSON
    request.send(dataJSON);
}

