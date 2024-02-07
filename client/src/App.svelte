<script>
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/home/Index.svelte";
  import Login from "./routes/login/Index.svelte";
  import Profile from "./routes/profile/Index.svelte";
  import TailWind from "./styles/TailWind.svelte";

  import User_message from "./routes/profile/UserMessage.svelte";

  let name = "NexaPulse";
  let login = "Login";
  let current_user_id = "3213123";

  export const url = "";
</script>

<Router {url}>
  <div>
    <Route path="/"><Home /></Route>
    <Route path="/login"><Login propName={login} /></Route>
    <Route path="/profile/:id" let:params>
      <Profile id={params.id} />
    </Route>
    <div />
  </div>
</Router>

<Router>
  <Route path="/user_message/:id" let:params>
    <User_message id={current_user_id} />
  </Route>
</Router>
