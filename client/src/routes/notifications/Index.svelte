<script>
  export let id;
  import Notis from "./notis.svelte";
  import { onMount } from "svelte";
  import { server, authToken, currentUser } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";

  // Define an array to store follow requests
  let followRequests = [];
  let isLoading = true; // Add a loading state

  // Fetch author's information based on authorId
  async function fetchAuthor(id) {
    try {
      const response = await fetch(`${server}/api/authors/${id}`);
      if (response.ok) {
        const authorData = await response.json();
        let userName = `${authorData.firstName} ${authorData.lastName}`; // Set the userName to the author's display name
        return userName;
      } else {
        console.error(
          "Failed to fetch author information:",
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error fetching author information:", error.message);
    }
  }

  onMount(async () => {
    const followRequestsEndpoint =
      server + `/api/follow/all/${get(currentUser).userId}`;
    const response = await fetchWithRefresh(followRequestsEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow requests");
    }

    const data = await response.json();

    // Update followRequests array
    data.forEach((item) => {
      let name = "";
      fetchAuthor(item.follower).then((name) => {
        // Use the retrieved name here
        name = name;
      });
      const followRequest = {
        id: item.follower,
        userId: item.follower,
        profileImageUrl:
          "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
        userName: item.follower,
        postTime: "1h ago",
      };
      followRequests.push(followRequest);
    });

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
