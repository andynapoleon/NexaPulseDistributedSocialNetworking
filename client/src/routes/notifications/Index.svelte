<script>
  export let id;
  import Notis from "./notis.svelte";
  import { onMount } from "svelte";
  import { server, authToken, currentUser } from "../../stores/stores.js";
  import { get } from "svelte/store";

  // Define an array to store follow requests
  let followRequests = [];
  let isLoading = true; // Add a loading state

  onMount(async () => {
    const followRequestsEndpoint = server + `/api/follow/all/${get(currentUser).userId}`;
    const response = await fetch(followRequestsEndpoint, {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      }
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow requests");
    }

    const data = await response.json();
    console.log("HEYYYY")
    console.log(data)

    // Update followRequests array
    followRequests = data.map(item => ({
      id: item.follower,
      profileImageUrl: "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
      userName: item.follower,
      postTime: "1h ago",
    }));

    isLoading = false; // Update loading state
  });
</script>

<main class="main" {id}>
  <div class="profile-layout">
    <div class="profile-widget"></div>
    <div class="posts">
      {#if isLoading}
        <p>Loading...</p>
      {:else}
        <Notis {followRequests} />
      {/if}
    </div>
  </div>
</main>

<style>
  @import "notiStyle.css";
</style>
