<script>
  import Post from "./Post.svelte";

  // Sample array of post objects - will do data fetching instead
  export let posts = [];
</script>

<div class="posts">
  {#each posts as { id, userName, postTime, content } (id)}
    <Post {userName} {postTime} {content} />
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
