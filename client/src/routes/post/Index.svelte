<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Posts from "../../widgets/Posts.svelte";
  import { onMount } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    currentUser,
    server,
  } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";
  // let isAuthenticated = false;

  function isValidGitHubLink(link) {
    // Regular expression to match GitHub user profile URLs
    var regex = /^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+$/;
    return regex.test(link);
  }

  function getGitHubUsername(link) {
    // Regular expression to match GitHub user profile URLs and extract the username
    var regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)$/;
    var match = link.match(regex);
    if (match) {
      return match[1]; // Return the username captured by the regex
    } else {
      return null; // Return null if the link is not a valid GitHub link
    }
  }
</script>

<main class="posts">
  <h1 class="text-[#0f6460] font-bold text-xl">Let's Create A Post!</h1>
  <br />
  <CreatePost />
  <h1 class="text-[#0f6460] font-bold text-xl">Explore New Posts</h1>
  <br />
  <Posts />
</main>

<style>
  .posts {
    padding-top: 7%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
