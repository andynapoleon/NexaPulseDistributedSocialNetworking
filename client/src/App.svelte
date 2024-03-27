<script>
  import { Router, Route } from "svelte-routing";
  import TailWind from "./styles/TailWind.svelte";
  import NavBar from "./components/NavBar.svelte";
  import SideBar from "./components/SideBar.svelte";
  import Home from "./routes/home/Index.svelte";
  import Profile from "./routes/profile/Index.svelte";
  import Notifications from "./routes/notifications/Index.svelte";
  import Login from "./routes/login/Index.svelte";
  import Friends from "./routes/friends/Index.svelte";
  import AllUsers from "./routes/allusers/Index.svelte";
  import ForYou from "./routes/foryou/Index.svelte";
  import AuthenticatedRoute from "./components/AuthenticatedRoute.svelte";
  import Post from "./routes/post/Index.svelte";
  import {
    mode,
    currentUser,
    authToken,
    hasNotifications,
    isLoginPage,
  } from "./stores/stores.js";

  // Sidebar menu items
  const menuItems = [
    { href: "/home", label: "Home" },
    { href: "/foryou", label: "For You" },
    { href: `/friends/${$currentUser.userId}`, label: "Friends" },
    { href: "/all_users", label: "Everyone" },
    { href: `/notifications/${$currentUser.userId}`, label: "Requests" },
    { href: "/", label: "Log Out" },
  ];

  // Routes
  const routes = {
    "/home": Home,
    "/foryou": ForYou,
    "/profile/:id": Profile,
    "/posts/:id": Post,
    "/notifications/:id": Notifications,
    "/friends/:id": Friends,
    "/all_users": AllUsers,
  };

  // Reactively set isLoginPage based on the current path
  let path = location.pathname;
  $isLoginPage = path === "/";

  export const url = "";
</script>

<!-- Main Layout -->
{#if !$isLoginPage}
  <SideBar items={menuItems}/>
  <NavBar />
{/if}

<!-- Router -->
<Router {url}>
  <Route path="/">
    <Login /></Route>
  {#each Object.keys(routes) as route}
    <Route path={route} let:params>
      <AuthenticatedRoute>
        <!-- Render the protected route component -->
        <svelte:component this={routes[route]} {params} />
      </AuthenticatedRoute>
    </Route>
  {/each}
</Router>

<style>
</style>
