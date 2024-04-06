<script>
  import { onMount } from "svelte";

  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get, writable } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { TruckSolid } from "flowbite-svelte-icons";

  export let profileImage;
  export let userId; // The user ID passed into the component
  export let userName = "HOHO HAHA";
  export let postTime = "1 min ago";
  // export let content = "wanted to follow you.";

  const currentUserId = $currentUser.userId;

  // Initialize alreadyFollowed as a writable store
  let alreadyFriended = Boolean(false);
  let rejectClicked = false;

  async function updateStatus() {
    // Check if the current user has already accepted the follow request

    const followEndpoint =
      server + `/api/follow/${currentUserId}?userId2=${userId}`;

    console.log("updateStatus");

    const response = await fetchWithRefresh(followEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const data = await response.json();

    console.log(
      "/api/follow/",
      { currentUserId },
      "?userId2=",
      { userId },
      ":",
      data
    );

    // Convert data.acceptedRequest to a boolean value
    const acceptedRequestBoolean = Boolean(data.acceptedRequest);

    // Set alreadyFriended to the boolean value
    alreadyFriended = acceptedRequestBoolean;

    console.log("alreadyFriended:", alreadyFriended);
  }

  onMount(async () => {
    await updateStatus(); // Wait for updateStatus to finish
  });

  async function acceptResponseButtonClicked() {
    const followRequest = {
      userId1: userId,
      userId2: currentUserId, //target user is the current user
    };
    const followEndpoint =
      server + `/api/follow/${currentUserId}?userId2=${userId}`;
    const headers = {
      Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
      "Content-Type": "application/json",
    };
    const response = await fetchWithRefresh(followEndpoint, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify(followRequest),
    });
    if (!response.ok) {
      throw new Error("Failed to confirm follow request");
    }
    updateStatus();
  }

  async function rejectResponseButtonClicked() {
    const followRequest = {
      userId1: userId,
      userId2: currentUserId, //target user
    };
    const followEndpoint =
      server + `/api/follow/${userId}?userId2=${currentUserId}`;
    const headers = {
      Authorization: `Bearer ${get(authToken)}`, // Include the token in the request headers
      "Content-Type": "application/json",
    };
    const response = await fetchWithRefresh(followEndpoint, {
      method: "DELETE",
      headers: headers,
      body: JSON.stringify(followRequest),
    });
    console.log("DELETE", response);
    if (!response.ok) {
      throw new Error("Failed to delete follow request");
    }
    rejectClicked = true;
  }
</script>

{#if !rejectClicked}
  <div class="post">
    <div class="content">
      <div class="left-column">
        <img
          class="profile-avatar"
          src="{profileImage},"
          alt="Profile Avatar"
        />
      </div>
      <div class="right-column">
        <div class="post-header">
          {#if alreadyFriended}
            <div class="already-accepted">{userName} wanted to follow you.</div>
          {:else}
            <strong>{userName} wanted to follow you.</strong>
          {/if}
          <span>{postTime}</span>
        </div>
        {#if alreadyFriended}
          <div class="actions">
            <accepted-button>Already Accepted</accepted-button>
          </div>
        {:else}
          <div class="actions">
            <button on:click={() => acceptResponseButtonClicked()}
              >Accept</button
            >
            <button on:click={() => rejectResponseButtonClicked()}
              >Reject</button
            >
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .post {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    width: 200%;
    font-size: large;
  }
  .content {
    display: flex;
  }

  /* Optional: Adjust styling for better presentation */
  .left-column {
    width: 80px;
    padding: 5px;
  }

  .right-column {
    flex: 1; /* Right column takes remaining space */
    padding: 10px;
  }

  .post-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    color: black;
  }
  .actions {
    display: flex;
    justify-content: right;
  }
  .already-accepted {
    color: #525252;
    font-weight: bold;
  }
  button {
    cursor: pointer;
    background-color: transparent;
    border: none;
    color: #008480;
    padding: 0;
    margin-right: 2%;
  }
  accepted-button {
    cursor: pointer;
    background-color: transparent;
    border: none;
    color: #525252;
    padding: 0;
    margin-right: 2%;
  }
  .profile-avatar {
    border-radius: 50%;
    width: 65px;
    height: 65px;
  }
</style>
