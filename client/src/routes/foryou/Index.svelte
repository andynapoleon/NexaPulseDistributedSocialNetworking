<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Posts from "../../widgets/FollowingPosts.svelte";
  import { onMount, onDestroy } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    server,
    followingPosts,
  } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";
  // let isAuthenticated = false;

  let streamType = "Following";

  // Function to fetch posts from the backend
  async function fetchPosts() {
    try {
      const response = await fetch(server + "/api/following-posts/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${$authToken}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Fetched posts:", data); // Log the fetched data
        $followingPosts = data;
      } else {
        console.error("Failed to fetch posts:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching posts:", error.message);
    }
  }

  function handleSubmit(event) {
    if (event.detail.currentStream == "Following") {
      fetchPosts();
    }
  }

  let fetchInterval;

  function pollForPosts() {
    fetchInterval = setInterval(() => {
      fetchPosts();
    }, 5000);
  }

  onMount(async () => {
    pollForPosts();
  });

  onDestroy(() => {
    clearInterval(fetchInterval);
  });

  onMount(() => {
    $isLoginPage = false;
    console.log(getCurrentUser());
    console.log(get(authToken));
  });
</script>

<main>
  <div class="sidebar" />
  <div class="navbar" />
  <div class="main-content">
    <h1 class="text-[#0f6460] font-bold text-xl">Let's Create A Post!</h1>
    <br />
    <CreatePost {streamType} on:submit={handleSubmit} />
    <h1 class="text-[#0f6460] font-bold text-xl">Posts For You</h1>
    <br />
    <Posts />
  </div>
</main>

<style>
  @import "foryouStyle.css";
</style>
