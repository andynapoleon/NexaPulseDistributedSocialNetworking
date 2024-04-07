<script>
  import { onMount, onDestroy } from "svelte";
  import Post from "./Post.svelte";
  import SharedPost from "./SharedPost.svelte";
  import { server } from "../stores/stores.js";
  import { posts } from "../stores/stores.js";
  import { authToken } from "../stores/stores.js";

  let fetchInterval;

  // Function to fetch posts from the backend
  async function fetchPosts() {
    try {
      const response = await fetch(server + "/api/public-posts/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${$authToken}`,
        },
      });
      const authToken1 = response.headers.get("Authorization");
      console.log(`Auth token: ${authToken1}`);
      if (response.ok) {
        const data = await response.json();
        console.log("Fetched posts:", data); // Log the fetched data
        $posts = data;
      } else {
        console.error("Failed to fetch posts:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching posts:", error.message);
    }
  }

  // Fetch posts when the component is mounted
  onMount(() => {
    fetchPosts();

    // Set up interval to periodically fetch new posts
    fetchInterval = setInterval(fetchPosts, 5000);
  });

  onDestroy(() => {
    // Clean up fetch interval when component is destroyed
    clearInterval(fetchInterval);
  });

  function handleChange(event) {
    if (event.detail.changeDetected == true) {
      fetchPosts();
    }
  }
</script>

<div class="posts">
  {#each $posts as post (post.id)}
    {#if !post.isShared}
      <Post {post} on:changed={handleChange} />
    {:else}
      <SharedPost {post} on:changed={handleChange} />
    {/if}
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
