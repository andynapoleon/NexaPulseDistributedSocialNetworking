<script>
  import { onMount } from "svelte";
  import Post from "./Post.svelte";
  import { server } from "../stores/stores.js";

  // Sample array of post objects - will do data fetching instead
  let profilePosts = [];
  export let authorId;

  // Function to fetch posts from the backend
  async function fetchPosts() {
    try {
      const response = await fetch(server + `/api/authors/posts/${authorId}/`);
      if (response.ok) {
        const data = await response.json();
        profilePosts = data;
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
  // onMount(fetchPosts);
</script>

<div class="posts">
  {#each profilePosts as post (post.id)}
    <Post {post} />
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
