<script>
  import { onMount } from "svelte";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  import { writable } from "svelte/store";
  import { fetchWithRefresh, extractUUID } from "../../utils/apiUtils.js";
  import ProfileWidget from "../profile/ProfileWidget.svelte";
  import { Link, navigate } from "svelte-routing";
  import { use } from "marked";

  export let user;
  if (user.id.includes("/")) {
    user.id = extractUUID(user.id);
  }
  const currentUserId = $currentUser.userId;
  const userId = user.id;
  const alreadyFollowed = writable(false);
  let alreadyFollowedValue;
  alreadyFollowed.subscribe((value) => {
    alreadyFollowedValue = value;
  });

  onMount(async () => {
    const followEndpoint = `${server}/api/follow/${userId}?userId2=${currentUserId}&senderHost=${server}&receiverHost=${user.host}`;
    console.log("currentUserId", currentUserId);
    console.log("target userId", userId);
    const response = await fetch(followEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${$authToken}`,
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const data = await response.json();
    alreadyFollowed.set(data.following);
    console.log(currentUserId, "is", data.following, "following", userId);
  });

  function navigateToProfile(event) {
    console.log("trigger");
    if (!event.target.classList.contains("follow-button")) {
      // Prevent the default behavior of the event (don't navigate)
      navigate(`/profile/${userId}`);
    }
  }
</script>

<!--<div class="user">
  <h3><strong>{user.displayName}</strong></h3>
  <p>Host: {user.host}</p>
  <img src={user.profileImage} alt={user.displayName + " profile pic"} />
  {#if currentUserId !== userId}
    {#if !$alreadyFollowed}
      <button class="follow-button" on:click={followButtonClick}>Follow</button>
    {:else}
      <button class="follow-button" on:click={followButtonClick}
        >Unfollow</button
      >
    {/if}
  {/if}
</div>-->

<div>
  <button class="button-profile-widget" on:click={navigateToProfile}>
    <ProfileWidget
      profileImage={user.profileImage}
      name={user.displayName}
      email={user.email}
      github={user.github}
      userId={user.id}
      host={user.host}
    />
  </button>
</div>

<style>
  @import "user.css";
</style>
