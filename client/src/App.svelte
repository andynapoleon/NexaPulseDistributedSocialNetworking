<script>
  import { Router, Route } from "svelte-routing";
  import TailWind from "./styles/TailWind.svelte";
  import * as Icon from "flowbite-svelte-icons";
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
    { href: "/all_users", label: "All Users" },
    { href: `/notifications/${$currentUser.userId}`, label: "Notifications" },
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
  <SideBar items={menuItems} let:item>
    {#if item.label === "Home"}
      <Icon.HomeSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "For You"}
      <Icon.PhoneSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "Messages"}
      <Icon.MessageCaptionSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "Create a post"}
      <Icon.PlusSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "Friends"}
      <Icon.ProfileCardOutline class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "All Users"}
      <Icon.UsersSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "Notifications"}
      <Icon.BellActiveSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
      <!-- If there are notifications, paint a dot -->
      {#if hasNotifications}
        <svg class="mt-2" width="12" height="12" viewBox="0 0 10 10">
          <circle cx="5" cy="5" r="5" fill="red" />
        </svg>
      {/if}
    {:else if item.label === "Settings"}
      <Icon.UserSettingsSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {:else if item.label === "Log Out"}
      <Icon.LockOpenSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
    {/if}
  </SideBar>
  <NavBar />
{/if}

<!-- Router -->
<Router {url}>
  <Route path="/">
    <Login /></Route
  >
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
