<script>
  import { Link } from "svelte-routing";
  import FriendWidget from "./friendWidget.svelte";
  import { onMount, onDestroy } from "svelte";
  import {
    authToken,
    isLoginPage,
    currentUser,
    server,
  } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  import { writable, get } from "svelte/store";

  let mode = writable(null);
  let isAuthenticated = false;

  let allFriends = [];
  let followed = [];
  let following = [];

  let currentList = [];

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

  async function fetchData() {
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
    allFriends = await friendsResponse.json();
    console.log("allFriends fetched:", allFriends);

    const followingResponse = await fetch(
      server + `/api/friends/following/${get(currentUser).userId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
        },
      }
    );
    if (!followingResponse.ok) {
      throw new Error("Failed to fetch following");
    }
    following = await followingResponse.json();
    console.log("following fetched:", following);

    const followedResponse = await fetch(
      server + `/api/friends/followed/${get(currentUser).userId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
        },
      }
    );
    if (!followedResponse.ok) {
      throw new Error("Failed to fetch followed");
    }
    followed = await followedResponse.json();
    console.log("followed fetched:", followed);

    currentList = allFriends;
  }

  let fetchInterval;

  function pollForPosts() {
      fetchInterval = setInterval(() => {
        fetchData();
      }, 10000);
    }

  onMount(async () => {
    fetchData();
    pollForPosts();
  });

  onDestroy(() => {
    clearInterval(fetchInterval);
  });

  //
  //sample = {
  //  "user_id": 1,
  //  "full_name": 1,
  //  "profileImageUrl": 1,
  //  "email": 1,
  //

  mode.set(1);

  const rowSize = writable(1); // Initialize with a default value
  function returnRowIndex() {
    if (window.innerWidth > 2200){
      rowSize.set(5);
    } else if(window.innerWidth > 1800) { // = 700/0.7
      rowSize.set(4);
    } else if (window.innerWidth > 1400){ // = 450/0.7
      rowSize.set(3);
    } else if (window.innerWidth > 1000){
      rowSize.set(2);
    } else {
      rowSize.set(1);
    }
    console.log("rowsize:", rowSize)
  }

  onMount(() => {
    returnRowIndex();
    window.addEventListener('resize', returnRowIndex);
  });
</script>

<main>
  <div class="sidebar" />
  <div class="navbar" />
  <div class="main-content">
    <div class="button-layout">
      <button
        class={$mode === 1 ? "selected-class-button" : "class-button"}
        on:click={() => switchMode(1)}>Friends</button
      >
      <button
        class={$mode === 2 ? "selected-class-button" : "class-button"}
        on:click={() => switchMode(2)}>Following</button
      >
      <button
        class={$mode === 3 ? "selected-class-button" : "class-button"}
        on:click={() => switchMode(3)}>Follower</button
      >
    </div>
    {#each Array(Math.ceil(currentList.length / $rowSize)) as _, rowIndex}
      <div class="profile-layout">
        {#each Array(Math.min($rowSize, currentList.length - rowIndex * $rowSize)) as _, colIndex}
          <Link to="/profile/{currentList[rowIndex * $rowSize + colIndex].user_id}">
            <div class="profile-widget">
              <FriendWidget
                profileImage={currentList[rowIndex * $rowSize + colIndex]
                  .profileImage}
                name={currentList[rowIndex * $rowSize + colIndex].full_name}
                email={currentList[rowIndex * $rowSize + colIndex].email}
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
