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
      const response = await fetchWithRefresh(
        `${server}/api/authors/${id.split("/").pop()}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${get(authToken)}`,
          },
        }
      );
      if (response.ok) {
        const authorData = await response.json();
        let userName = `${authorData.displayName}`; // Set the userName to the author's display name
        let profileImage = `${authorData.profileImage}`;
        return {
          userName: authorData.displayName,
          profileImage: authorData.profileImage,
        };
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

    // Define an async function to execute asynchronous operations sequentially
    async function processFollowRequests(data) {
      const follows = [];
      for (const item of data) {
        try {
          const { userName, profileImage } = await fetchAuthor(item.follower);
          const followRequest = {
            id: item.follower.split("/").pop(),
            userId: item.follower.split("/").pop(),
            profileImage: profileImage,
            userName: userName,
            postTime: "1h ago",
          };
          follows.push(followRequest);
        } catch (error) {
          console.error("Error fetching author:", error);
        }
      }
      followRequests = follows;
    }

    // Call the async function and handle the result
    processFollowRequests(data).then((followRequests) => {
      // Now you have the followRequests array ready to use
      console.log(followRequests);
    });

    isLoading = false; // Update loading state
  });
</script>

<main>
  <div class="sidebar" />
  <div class="navbar" />
  <div class="main-content" {id}>
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
  </div>
</main>

<style>
  @import "notiStyle.css";
</style>
