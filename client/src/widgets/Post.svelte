<script>
  // Props passed to the component
  export let userName = "User Name";
  export let postTime = "Just now";
  export let content = "Here is some post content.";
  let likes = 5;

  // Edit post function
  function editPost() {
    alert("I am editing a post");
  }
</script>

<div class="post">
  <div class="post-header">
    <strong>{userName}</strong>
    <span>{postTime}</span>
  </div>
  <div class="post-content">
    {content}
  </div>
  <div class="actions">
    <button>Like</button>
    <button>Share</button>
    <button on:click={editPost}>Edit</button>
    <span>Likes: {likes}</span>
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
  .post-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    color: black;
  }
  .post-content {
    margin-bottom: 12px;
  }
  .actions {
    display: flex;
    justify-content: left;
  }
  button {
    cursor: pointer;
    background-color: transparent;
    border: none;
    color: #007bff;
    padding: 0;
    margin-right: 2%;
  }
</style>
