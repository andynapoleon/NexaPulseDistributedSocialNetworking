<script>
  import { onMount } from "svelte";
  import Post from "./Post.svelte";
  import {
    server,
    authToken,
    isLoginPage,
    currentUser,
  } from "../stores/stores.js";
  import { writable, get } from "svelte/store";

  // Sample array of post objects - will do data fetching instead
  let profilePosts = [];
  export let authorId;

  // Function to fetch posts from the backend
  async function fetchPosts() {
    console.log("fetching posts")
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

  // Function to fetch posts from the backend as a STRANGER(can't see FRIENDS posts)
  async function fetchPostsAsStranger() {
    console.log("fetching posts as stranger")
    try {
      const response = await fetch(server + `/api/authors/posts/${authorId}/asStranger`);
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

  // Function to check if current user is a stranger
  let beFriend = false
  async function fetchFriends() {
    const friendsResponse = await fetch(
      server + `/api/friends/friends/${get(currentUser).userId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
        },
      }
    );
    if (!friendsResponse.ok) {
      throw new Error("Failed to fetch friends");
    }
    let allFriends = await friendsResponse.json();
    for (let i = 0; i < allFriends.length; i++) {
      if (authorId == allFriends[i].user_id){
        beFriend = true
      }
    }
    console.log("beFriend:", beFriend)
  }

  // Fetch posts when the component is mounted
  onMount(async () => {
    await fetchFriends()
    
    if (beFriend){
      fetchPosts();
    } else {
      fetchPostsAsStranger();
    }
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
