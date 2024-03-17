<script>
  import { onMount } from "svelte";
  import { authToken, server, currentUser } from "../../stores/stores.js";
  import User from "./User.svelte"

  // Define reactive variables
  let loading = true;
  let allUsers = [];

  // Get all users
  async function getAllUsers() {
    const res_nodes = await fetch(server + "/api/nodes", {
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

    // TODO:loop through other nodes to get remote authors
    for (let node of nodes.items) {
      console.log("SERVER HERE: ", node.host);
      const authString = `${node.username}:${node.password}`;
      const encodedAuthString = btoa(authString);
      // Send info of author to the server in the node
      let authorData = {
        id: $currentUser.userId,
        displayName: $currentUser.name,
        email: $currentUser.email,
        password: "i450959540943809",
        github: $currentUser.github,
      }
      console.log(authorData)
      const sendAuthorResponse = await fetch(
        node.host + `/api/authors/new/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            body: JSON.stringify(authorData)
          },
        }
      );
      // Get all remote authors 
      const res2 = await fetch(
        node.host + `/api/authors?request_host=${encodeURIComponent(server)}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Basic ${encodedAuthString}`,
          },
        }
      );
      const remoteAuthors = await res2.json();
      if (remoteAuthors.items) allAuthors.push(...remoteAuthors.items);
    }
    res_json.items.push(...allAuthors);
    console.log(res_json);

    return res_json;
  }

  // Fetch all users when the component is mounted
  onMount(async () => {
    // Fetch all users
    allUsers = await getAllUsers();
    // Update loading state
    loading = false;
  });
</script>

<div class="all-users">
  {#if loading}
    <p>Loading...</p>
  {:else}
    {#each allUsers.items as user}
      <User {user} />
    {/each}
  {/if}
</div>

<style>
  .all-users {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    color: black;
    padding-left: 25%;
    padding-top: 10%;
  }
</style>
