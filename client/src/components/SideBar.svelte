<script lang="ts">
  export let items = []; // expects an array of items for the sidebar
  import { onMount, onDestroy } from "svelte";
  import * as Icon from "flowbite-svelte-icons";

  import { writable } from "svelte/store"; // Import writable store
  import { link, navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  import { authToken, isLoginPage, currentUser } from "../stores/stores.js"; // Import currentUser from stores

  let currentSelection = localStorage.getItem("currentSelection") || "/home";
  console.log("Current Selection HERE:", currentSelection);

  // Logout function
  function handleLogout() {
    $authToken = "";
    $isLoginPage = true;
    navigate("/");
  }

  function onClickHandler(link) {
    navigate(link);
    currentSelection = link;
    localStorage.setItem("currentSelection", currentSelection);
    console.log("Current Selection:", localStorage.getItem("currentSelection"));
    // /home
    // /foryou
    // /friends/...
    // /all_users
    // /notifications/...
    handleHomeClass();
    handleAllUsersClass();
    handleForyouClass();
    handleFriendsClass();
    handleNotificationClass();
  }

  const homeSelected = writable("selected-menu-item");
  function handleHomeClass() {
    if (currentSelection.includes("/home")) {
      homeSelected.set("selected-menu-item");
    } else {
      console.log("selcted!!!");
      homeSelected.set("menu-item");
    }
  }

  const foryouSelected = writable("menu-item");
  function handleForyouClass() {
    if (currentSelection.includes("/foryou")) {
      foryouSelected.set("selected-menu-item");
    } else {
      console.log("selcted!!!");
      foryouSelected.set("menu-item");
    }
  }

  const friendsSelected = writable("menu-item");
  function handleFriendsClass() {
    if (currentSelection.includes("/friends")) {
      friendsSelected.set("selected-menu-item");
    } else {
      console.log("selcted!!!");
      friendsSelected.set("menu-item");
    }
  }

  const allUsersSelected = writable("menu-item");
  function handleAllUsersClass() {
    if (currentSelection.includes("/all")) {
      allUsersSelected.set("selected-menu-item");
    } else {
      console.log("selcted!!!");
      allUsersSelected.set("menu-item");
    }
  }

  const notificationsSelected = writable("menu-item");
  function handleNotificationClass() {
    if (currentSelection.includes("/notifications")) {
      notificationsSelected.set("selected-menu-item");
    } else {
      console.log("noti selcted!!!");
      notificationsSelected.set("menu-item");
    }
  }

  let sidebarClass = ""; // Initialize the sidebar class variable

  function updateSidebarClass() {
    var list = document.querySelectorAll("aside");
    // console.log("sideBar width:", list[0].offsetWidth)

    if (window.innerWidth > 1695) {
      // = 200/0.118
      sidebarClass = "bigSidebar";
    } else if (window.innerWidth > 1017) {
      //1017
      sidebarClass = "midSidebar";
    } else {
      sidebarClass = "smallSidebar";
    }
    console.log("change to ->", sidebarClass);
  }

  // Call toggleLabelVisibility on mount and remove listener on destroy
  onMount(() => {
    // Initial call
    handleHomeClass();
    handleAllUsersClass();
    handleForyouClass();
    handleFriendsClass();
    handleNotificationClass();
    updateSidebarClass();
    window.addEventListener("resize", updateSidebarClass);
    window.addEventListener("click", handleNotificationClass);
  });

  onDestroy(() => {
    window.removeEventListener("resize", updateSidebarClass);
  });

  console.log("Window Width:", screen.width);
  console.log("Window Height:", window.innerHeight);
</script>

<aside class={sidebarClass}>
  <nav>
    <ul>
      {#each items as item}
        <div class="container">
          {#if item.label === "Home"}
            <button
              class={$homeSelected}
              on:click={() => onClickHandler(`${item.href}`)}
            >
              <Icon.HomeSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "For You"}
            <button
              class={$foryouSelected}
              on:click={() => onClickHandler(`${item.href}`)}
            >
              <Icon.PhoneSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Friends"}
            <button
              class={$friendsSelected}
              on:click={() => onClickHandler(`${item.href}`)}
            >
              <Icon.ProfileCardSolid
                class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]"
              />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Everyone"}
            <button
              class={$allUsersSelected}
              on:click={() => onClickHandler(`${item.href}`)}
            >
              <Icon.UsersSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Requests"}
            <button
              class={$notificationsSelected}
              on:click={() => onClickHandler(`${item.href}`)}
            >
              <Icon.BellActiveSolid
                class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]"
              />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Log Out"}
            <button class="menu-item" on:click={handleLogout}>
              <Icon.LockOpenSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {/if}
        </div>
      {/each}
    </ul>
  </nav>
</aside>

<style>
  @import "SideBarStyle.css";
</style>
