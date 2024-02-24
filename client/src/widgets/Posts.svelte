<script>
  import { onMount } from 'svelte';
  import Post from "./Post.svelte";
  import { server } from "../stores/stores.js";

  // Sample array of post objects - will do data fetching instead
  let posts = [];

  // Function to fetch posts from the backend
  async function fetchPosts() {
    try {
      const response = await fetch(server+'/api/posts/');
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched posts:', data); // Log the fetched data
        posts = data;
      } else {
        console.error('Failed to fetch posts:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching posts:', error.message);
    }
  }

  // Fetch posts when the component is mounted
  onMount(() => {
    fetchPosts();
  });
</script>

<!-- <div class="posts">
  {#each posts as { id, userName, postTime, title, content } (id)}
    <Post {userName} {postTime} {title} {content} />
  {/each}
</div> -->

<div class="posts">
  {#each posts as post (post.id)}
    <Post {...post} />
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
