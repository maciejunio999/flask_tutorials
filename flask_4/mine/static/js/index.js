/*
    main JavaScript file, gets everything working
*/

import { People } from "./people.js";
import { Tasks } from "./tasks.js";
import { DebugForm } from "./debug.js";


function main() {
  new People();
  new Tasks();
  if (document.querySelector(".debug-card")) {
    const debug = new DebugForm();
    debug.showResponse("");
  }
}

main();
