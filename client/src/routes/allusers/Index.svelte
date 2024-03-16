<script>
  import { onMount } from "svelte";
  import { authToken, server } from "../../stores/stores.js";

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
      console.log(node);
      const authString = `${node.username}:${node.password}`;
      const encodedAuthString = btoa(authString);
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

<h1>Hi</h1>

<div class="all-users">
  {#if loading}
    <p>Loading...</p>
  {:else}
    {#each allUsers.items as user}
      <div class="user">
        <h3><strong>{user.displayName}</strong></h3>
        <p>Host: {user.host}</p>
        <img src={user.profileImage} alt={user.displayName + " profile pic"} />
        <button class="follow-button">Follow</button>
      </div>
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

  .user {
    border: 1px solid #ccc;
    padding: 10px;
    width: 300px;
    color: black;
  }

  img {
    max-width: 100%;
    height: auto;
  }

  .follow-button {
    background-color: teal;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .follow-button:hover {
    background-color: darkcyan;
  }
</style>
