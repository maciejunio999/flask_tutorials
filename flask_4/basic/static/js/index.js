import { People } from "./people.js";
import { Notes } from "./notes.js";
import { DebugForm } from "./debug.js";


function main() {
  new People();
  new Notes();
  /*
    consequentially, you’re conditionally instantiating DebugForm only if there’s a .debug-card element on the page inside of main()
    otherwise, there’s no need to have the debug functionality present
  */
  if (document.querySelector(".debug-card")) {
    const debug = new DebugForm();
    debug.showResponse("");
  }
}

main();