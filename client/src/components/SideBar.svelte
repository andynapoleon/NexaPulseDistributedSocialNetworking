<script lang="ts">
  export let items = []; // expects an array of items for the sidebar
  import { onMount, onDestroy } from "svelte";
  import * as Icon from "flowbite-svelte-icons";
  import { writable } from "svelte/store"; // Import writable store
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  import { authToken, isLoginPage, currentUser } from "../stores/stores.js"; // Import currentUser from stores

  // Logout function
  function handleLogout() {
    $authToken = "";
    $isLoginPage = true;
    navigate("/");
  }

  let sidebarClass = ""; // Initialize the sidebar class variable

  function updateSidebarClass() {
    if (window.innerWidth > 1700) {
      sidebarClass = "bigSidebar";
    } else if (window.innerWidth > 1017) {
      sidebarClass = "midSidebar";
    } else {
      sidebarClass = "smallSidebar";
    }
    console.log("change to ->", sidebarClass);
  }

  // Call toggleLabelVisibility on mount and remove listener on destroy
  onMount(() => {
    // Initial call
    updateSidebarClass();
    window.addEventListener("resize", updateSidebarClass);
  });

  onDestroy(() => {
    window.removeEventListener("resize", updateSidebarClass);
  });

  console.log("Window Width:", window.innerWidth);
  console.log("Window Height:", window.innerHeight);
</script>

<aside class={sidebarClass}>
  <nav>
    <ul>
      {#each items as item}
        <div class="container">
          {#if item.label === "Home"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.HomeSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "For You"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.PhoneSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Friends"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.ProfileCardSolid
                class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]"
              />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Everyone"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.UsersSolid class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]" />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Requests"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.BellActiveSolid
                class="pt-3 w-[2em] h-[2em] text-[#C2C2C2]"
              />
              {#if sidebarClass === "bigSidebar"}
                <span>{item.label}</span>
              {/if}
            </button>
          {:else if item.label === "Settings"}
            <button class="menu-item" on:click={() => navigate(`${item.href}`)}>
              <Icon.UserSettingsSolid
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
