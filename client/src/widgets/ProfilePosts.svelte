<script>
  import { onMount } from "svelte";
  import Post from "./Post.svelte";
  import SharedPost from "./SharedPost.svelte";
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
    console.log("fetching posts");
    try {
      const response = await fetch(server + `/api/authors/posts/${authorId}/`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${$authToken}`,
        },
      });
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

  // Function to fetch posts from the backend
  async function fetchPostsAsHimself() {
    console.log("fetching posts");
    try {
      const response = await fetch(
        server + `/api/authors/posts/${authorId}/asHimself`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${$authToken}`,
          },
        }
      );
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
    console.log("fetching posts as stranger");
    console.log(`AUTHORID: ${authorId}`);
    try {
      const response = await fetch(
        server + `/api/authors/posts/${authorId}/asStranger`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${$authToken}`,
          },
        }
      );
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
  let beFriend = false;
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
      if (authorId == allFriends[i].user_id) {
        beFriend = true;
      }
    }
    console.log("beFriend:", beFriend);
  }

  // Fetch posts when the component is mounted
  onMount(async () => {
    await fetchFriends();
    if (authorId == get(currentUser).userId) {
      fetchPostsAsHimself();
    } else {
      if (beFriend) {
        fetchPosts();
      } else {
        fetchPostsAsStranger();
      }
    }
  });

  function handleChange(event) {
    if (event.detail.changeDetected == true) {
      if (authorId == get(currentUser).userId) {
        fetchPostsAsHimself();
      } else {
        if (beFriend) {
          fetchPosts();
        } else {
          fetchPostsAsStranger();
        }
      }
    }
  }
</script>

<div class="posts">
  {#each profilePosts as post (post.id)}
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
