<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  let content = "";

  function sharePost() {
    if (content.trim() !== "") {
      dispatch("confirm", { content });
    } else {
      content = "Check out this post!";
      dispatch("confirm", { content });
    }
  }

  function cancelShare() {
    dispatch("cancel");
  }
</script>

<div class="share-popup">
  <textarea bind:value={content} placeholder="Enter your shared post content"
  ></textarea>
  <div class="buttons">
    <button on:click={sharePost}>Share</button>
    <button on:click={cancelShare}>Cancel</button>
  </div>
</div>

<style>
  .share-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 9999;
  }

  textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 10px;
    resize: none;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
  }

  .buttons {
    display: flex;
    justify-content: flex-end;
  }

  button {
    cursor: pointer;
    padding: 8px 16px;
    margin-left: 10px;
    border: none;
    border-radius: 4px;
    background-color: #008480;
    color: white;
  }
</style>
