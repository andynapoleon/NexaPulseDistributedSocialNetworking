<script>
  // Props passed to the component
  export let profileImageUrl =  "default-profile.png";
  export let userName = "HOHO HAHA";
  export let postTime = "1 min ago";
  export let content = "wanted to follow you."

  function responseButtonClicked(response) {
    alert(response);
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
        <button on:click={() => responseButtonClicked("Accept")}>Accept</button>
        <button on:click={() => responseButtonClicked("Accept")}>Reject</button>
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
    padding: 10px;
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
    width: 50px;
    height: 50px;
  }
</style>
