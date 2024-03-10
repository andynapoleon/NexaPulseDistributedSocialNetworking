<script>
  import { onMount } from "svelte";
  import Post from "./Post.svelte";
  import SharedPost from "./SharedPost.svelte";
  import { server } from "../stores/stores.js";
  import { followingPosts } from "../stores/stores.js";
  import { authToken } from "../stores/stores.js";

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

  // Fetch posts when the component is mounted
  onMount(() => {
    fetchPosts();
  });

  function handleChange(event) {
    if (event.detail.changeDetected == true) {
      fetchPosts();
    }
  }
</script>

<div class="posts">
  {#each $followingPosts as post (post.id)}
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
