<script>
  import { onMount } from "svelte";
  import { authToken, server } from "../../stores/stores.js";

  onMount(async () => {
    // fetch
    const allUsers = await getAllUsers();
  });

  // Get all users
  async function getAllUsers() {
    const res_nodes = await fetch(server + "/api/nodes", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$authToken}`
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
      const authString = `${node.username}:${node.password}`;
      const encodedAuthString = btoa(authString);
      const res2 = await fetch(node.host + "/api/authors", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Basic ${encodedAuthString}`,
          host: server,
        },
      });
      const remoteAuthors = await res2.json();
      if (remoteAuthors.items) allAuthors.push(...remoteAuthors.items);
    }
    res_json.items.push(...allAuthors);
    console.log(res_json);

    return res_json;
  }
</script>
