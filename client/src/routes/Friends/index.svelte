<script>
  import { Link } from 'svelte-routing';
  import FriendWidget from "../Friends/friendWidget.svelte";
  import { onMount } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    server,
    refreshToken,
  } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  import { writable } from 'svelte/store';

  let mode = writable(null);
  let isAuthenticated = false;

  let allFriends = [];
  let followed = [];
  let following = [];

  function switchMode(newMode) {
    mode.set(newMode);
    switch (newMode) {
      case 1:
        currentList = allFriends;
        break;

      case 2:
        currentList = following;
        break;

      case 3:
        currentList = followed;
        break;

      default:
        currentList = allFriends;
    }
  }

  onMount(async () => {
    isAuthenticated = $authToken !== "";
    if (!isAuthenticated) {
      $isLoginPage = true;
      navigate("/");
    }
    const friendsResponse = await fetch(server + `/api/friends/friends/${getCurrentUser().userId()}`, {
      method: "GET",
    });
    if (!friendsResponse.ok) {
      throw new Error("Failed to fetch friends");
    }
    allFriends = await friendsResponse.json();

    const followingResponse = await fetch(server + `/api/friends/following/${getCurrentUser().userId()}`, {
      method: "GET",
    });
    if (!followingResponse.ok) {
      throw new Error("Failed to fetch friends");
    }
    following = await followingResponse.json();

    const followedResponse = await fetch(server + `/api/friends/followed/${getCurrentUser().userId()}`, {
      method: "GET",
    });
    if (!followedResponse.ok) {
      throw new Error("Failed to fetch friends");
    }
    followed = await followedResponse.json();
    
  });

  //
  //let sample = {
  //  "user_id": 1,
  //  "full_name": 1,
  //  "profileImageUrl": 1,
  //  "email": 1,
  //

  let currentList = allFriends;
  mode.set(1)
</script>

<main>
  <div class="sidebar"/>
  <div class="navbar"/>
  <div class="main-content">
    <div class="button-layout">
      <button class={$mode === 1 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(1)}>Friends</button>
      <button class={$mode === 2 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(2)}>Following</button>
      <button class={$mode === 3 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(3)}>Follower</button>
    </div>
    {#each Array(Math.ceil(currentList.length/5)) as _, rowIndex}
      <div class="profile-layout">
        {#each Array(Math.min(5, currentList.length - rowIndex * 5)) as _, colIndex}
          <Link to="/profile/{currentList[rowIndex * 5 + colIndex].id}">
            <div class="profile-widget">
              <FriendWidget
                profileImageUrl= {currentList[rowIndex * 5 + colIndex].profileImageUrl}
                name = {currentList[rowIndex * 5 + colIndex].full_name}
                email = {currentList[rowIndex * 5 + colIndex].email}
              />
            </div>
          </Link>
        {/each}
      </div>
    {/each}
  </div>
</main>

<style>
  @import "friendStyle.css";
</style>