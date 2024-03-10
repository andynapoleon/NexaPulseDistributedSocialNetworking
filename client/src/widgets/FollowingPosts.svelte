<script>
  import { onMount } from "svelte";
  import Post from "./Post.svelte";
  import SharedPost from "./SharedPost.svelte";
  import { server } from "../stores/stores.js";
  import { posts } from "../stores/stores.js";
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
  });
</script>

<div class="posts">
  {#each $posts as post (post.id)}
    {#if !post.isShared}
      <Post {post} />
    {:else}
      <SharedPost {post} />
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
