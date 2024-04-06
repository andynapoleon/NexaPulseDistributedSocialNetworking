<script>
  import { onMount } from "svelte";
  import { authToken, server, currentUser } from "../../stores/stores.js";
  import User from "./User.svelte";
  import { Link, navigate } from "svelte-routing";
  import { writable } from "svelte/store";

  // Define reactive variables
  let loading = true;
  let allUsers = [];

  // Get all users
  async function getAllUsers() {
    const res_nodes = await fetch(server + "/api/nodes/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$authToken}`,
      },
    });
    // Array of host, password, username
    const nodes = await res_nodes.json();

    // get local authors from the server
    const res = await fetch(server + "/api/authors", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$authToken}`,
      },
    });
    const res_json = await res.json();
    const allAuthors = [];

    // // TODO:loop through other nodes to get remote authors
    // for (let node of nodes.items) {
    //   console.log("SERVER HERE: ", node.host);
    //   const authString = `${node.username}:${node.password}`;
    //   const encodedAuthString = btoa(authString);
    //   // Get all remote authors
    //   const res2 = await fetch(
    //     node.host + `/authors?request_host=${encodeURIComponent(server)}`,
    //     {
    //       method: "GET",
    //       headers: {
    //         "Content-Type": "application/json",
    //         Authorization: `Basic ${encodedAuthString}`,
    //       },
    //     }
    //   );
    //   const remoteAuthors = await res2.json();
    //   if (remoteAuthors.items) allAuthors.push(...remoteAuthors.items);
    // }
    res_json.items.push(...allAuthors);
    console.log(res_json);

    return res_json;
  }

  const rowSize = writable(1); // Initialize with a default value
  function returnRowIndex() {
    if (window.innerWidth > 2200) {
      rowSize.set(5);
    } else if (window.innerWidth > 1800) {
      // = 700/0.7
      rowSize.set(4);
    } else if (window.innerWidth > 1400) {
      // = 450/0.7
      rowSize.set(3);
    } else if (window.innerWidth > 1000) {
      rowSize.set(2);
    } else {
      rowSize.set(1);
    }
    console.log("rowsize:", rowSize);
  }

  onMount(() => {
    returnRowIndex();
    window.addEventListener("resize", returnRowIndex);
  });

  // Fetch all users when the component is mounted
  onMount(async () => {
    // Fetch all users
    allUsers = await getAllUsers();
    // Update loading state
    loading = false;
    console.log("allUsers:", allUsers);
  });
</script>

<main>
  <div class="sidebar" />
  <div class="navbar" />
  <div class="main-content">
    <div class="all-users">
      {#if loading}
        <p>Loading...</p>
      {:else}
        {#each Array(Math.ceil(allUsers.items.length / $rowSize)) as _, rowIndex}
          <div class="profile-layout">
            {#each Array(Math.min($rowSize, allUsers.items.length - rowIndex * $rowSize)) as _, colIndex}
              <div class="profile-widget">
                <User user={allUsers.items[rowIndex * $rowSize + colIndex]} />
              </div>
            {/each}
          </div>
        {/each}
        <!-- {#each allUsers.items as user}
          <User {user} />
        {/each} -->
      {/if}
    </div>
  </div>
</main>

<style>
  @import "allusersStyle.css";
</style>
