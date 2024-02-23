<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  let postTitle = "";
  let postContent = "";

  // Function to handle form submission
  function submitPost() {
    if (postContent.trim() === "") {
      // Prevent submission of empty content
      console.error("Post content cannot be empty");
      return;
    }
    dispatch("createpost", { title: postTitle, content: postContent });
    postContent = ""; // Reset input field after submission
    postTitle = ""; // Reset input field after submission
  }

</script>

<div class="create-post">
  <input type="text" class="post-title" placeholder="Title" bind:value={postTitle}>
  <textarea class="post-content" placeholder="What's on your mind?" bind:value={postContent}></textarea>
  <input type="file" class="post-image" accept="image/*">
  <button class="post-button" on:click={submitPost}>Post</button>
</div>

<style>
  .create-post {
    display: flex;
    flex-direction: column;
    justify-content: right;
    margin-bottom: 20px;
  }
  .post-title,
  .post-content,
  .post-image {
    color: black;
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background-color: teal;
    color: white;
    font-weight: bold;
    width: 7%;
    margin-left: 93%;
  }
</style>
