<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let postContent = "";

  // Function to handle form submission
  function submitPost() {
    if (postContent.trim() === "") {
      // Prevent submission of empty content
      console.error("Post content cannot be empty");
      return;
    }
    dispatch("createpost", { content: postContent });
    postContent = ""; // Reset input field after submission
  }
</script>

<div class="create-post">
  <textarea placeholder="What's on your mind?" bind:value={postContent}
  ></textarea>
  <button on:click={submitPost}>Post</button>
</div>

<style>
  .create-post {
    display: flex;
    flex-direction: column;
    justify-content: right;
    margin-bottom: 20px;
  }
  textarea {
    color: black;
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    resize: vertical; /* Allows the user to vertically resize the textarea */
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
