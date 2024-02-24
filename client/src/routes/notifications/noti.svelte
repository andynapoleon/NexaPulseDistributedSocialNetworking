<script>
  // Props passed to the component
  export let profileImageUrl =  "default-profile.png";
  import { currentUser, server, authToken } from "../../stores/stores.js";
  import { get } from "svelte/store";
  export let userName = "HOHO HAHA";
  export let postTime = "1 min ago";
  export let content = "wanted to follow you."
  import { fetchWithRefresh } from "../../utils/apiUtils.js";

  export let userId; // The user ID passed into the component

  const currentUserId = get(currentUser).userId; 

  async function acceptResponseButtonClicked(){
    alert("accepted")
  }
  async function rejectResponseButtonClicked() {
    console.log("reject clicked")
    console.log("currentUserId", currentUserId)
    console.log("userId", userId)
    const followRequest = {
      userId1 : currentUserId,
      userId2 : userId, //target user
    }; 
    const followEndpoint = server + `/api/follow/${currentUserId}?userId2=${userId}`;
    const headers = {
      'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      'Content-Type': 'application/json'
    };
    const response = await fetchWithRefresh(followEndpoint, {
      method: "DELETE",
      headers: headers,
      body: JSON.stringify(followRequest),
    });
    if (!response.ok) { 
      throw new Error("Failed to delete follow request");
    }
    // Reload the page after successful deletion
    location.reload();
  }
</script>

<div class="post">
  <div class="content">
    <div class="left-column">
      <img class="profile-avatar" src={profileImageUrl}, alt="Profile Avatar" />
    </div>
    <div class="right-column">
      <div class="post-header">
        <strong>{userName} {content}</strong>
        <span>{postTime}</span>
      </div>
      <div class="actions">
        <button on:click={() => acceptResponseButtonClicked()}>Accept</button>
        <button on:click={() => rejectResponseButtonClicked()}>Reject</button>
      </div>
    </div>
  </div>
</div>

<style>
  .post {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 3%;
    color: black;
    width: 100%;
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
  button {
    cursor: pointer;
    background-color: transparent;
    border: none;
    color: #008480;
    padding: 0;
    margin-right: 2%;
  }
  .profile-avatar {
    border-radius: 50%;
    width: 65px;
    height: 65px;
  }
</style>
