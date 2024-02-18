<script>
  import { Router, Route } from "svelte-routing";
  import TailWind from "./styles/TailWind.svelte";
  import * as Icon from "flowbite-svelte-icons";
  import NavBar from "./components/NavBar.svelte";
  import SideBar from "./components/SideBar.svelte";
  import Home from "./routes/home/Index.svelte";
  import Profile from "./routes/profile/Index.svelte";
  import UserMessage from "./routes/messages/UserMessage.svelte";
  import Notifications from "./routes/notifications/Index.svelte";
  import Login from "./routes/login/Index.svelte";
  import {
    mode,
    currentUser,
    token,
    hasNotifications,
  } from "./stores/stores.js";

  // Global variables
  $hasNotifications = true;
  $currentUser.userId = "123";

  // Sidebar menu items
  const menuItems = [
    { href: "/", label: "Home" },
    { href: `/messages/${$currentUser.userId}`, label: "Messages" },
    { href: "/makepost", label: "Create a post" },
    { href: "/friends", label: "Friends" },
    { href: `/notifications/${$currentUser.userId}`, label: "Notifications" },
    { href: "/settings", label: "Settings" },
  ];

  export const url = "";
</script>

<!-- Main Layout -->
<SideBar items={menuItems} let:item>
  {#if item.label === "Home"}
    <Icon.HomeSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
  {:else if item.label === "Messages"}
    <Icon.MessageCaptionSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
  {:else if item.label === "Create a post"}
    <Icon.PlusSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
  {:else if item.label === "Friends"}
    <Icon.ProfileCardOutline class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
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
  {/if}
</SideBar>
<NavBar />

<!-- Router -->
<Router {url}>
  <div>
    <Route path="/">
      <Home /></Route
    >
    <Route path="/login">
      <Login /></Route
    >
    <Route path="/profile/:id" let:params>
      <div class="content">
        <Profile id={params.id} />
      </div>
    </Route>
    <Route path="/messages/:id" let:params>
      <div class="content">
        <UserMessage />
      </div>
    </Route>
    <Route path="/notifications/:id" let:params>
      <div class="content">
        <Notifications id={$currentUser.userId} />
      </div>
    </Route>
  </div>
</Router>

<style>
</style>
