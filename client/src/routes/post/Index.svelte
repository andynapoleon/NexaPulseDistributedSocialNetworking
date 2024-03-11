<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Post from "../../widgets/Post.svelte";
  import { onMount, beforeUpdate } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    currentUser,
    server,
  } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";

  export let params;
  let postId = params.id;
  let post;

  async function fetchPostById() {
    console.log("fetching post by ID");
    try {
      const response = await fetch(`${server}/api/posts/${postId}`);
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        post = data;
      } else {
        console.error("Failed to fetch post:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching post:", error.message);
    }
  }

  onMount(fetchPostById);
</script>

<main class="posts">
  {#if post}
    <Post {post}></Post>
  {:else}
    <p>Loading post...</p>
  {/if}
</main>

<style>
  .posts {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
