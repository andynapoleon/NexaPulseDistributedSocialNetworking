<script>
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/home/Index.svelte";
  import Login from "./routes/login/Index.svelte";
  import Profile from "./routes/profile/Index.svelte";

  let name = "NexaPulse";
  let login = "Login";
  let current_user_id = "3213123";

  export const url = "";
</script>

<Router {url}>
  <nav>
    <Link to="/">Home</Link>
    <Link to="/login">Login</Link>
    <Link to="/profile/{current_user_id}">Profile</Link>
  </nav>
  <div>
    <Route path="/"><Home propName={name} /></Route>
    <Route path="/login"><Login propName={login} /></Route>
    <Route path="/profile/:id" let:params>
      <Profile id={params.id} />
    </Route>
    <div />
  </div>
</Router>
